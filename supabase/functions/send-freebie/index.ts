// Supabase Edge Function: send-freebie
// Deploy with: supabase functions deploy send-freebie

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

// Brevo API Key from Secrets
const BREVO_API_KEY = Deno.env.get("BREVO_API_KEY");
const SUPABASE_URL = Deno.env.get("SUPABASE_URL");
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  try {
    const { email, source = 'landing_page' } = await req.json();

    if (!email || !email.includes("@")) {
      return new Response(
        JSON.stringify({ error: "Invalid email address" }),
        { status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    // 1. Initialize Supabase client (Backup DB)
    const supabase = createClient(SUPABASE_URL!, SUPABASE_SERVICE_ROLE_KEY!);

    // Insert or update waitlist entry
    const { data: entry, error: dbError } = await supabase
      .from("waitlist")
      .upsert({ email, status: 'pending', source }, { onConflict: 'email' })
      .select("confirmation_token, status")
      .single();

    if (dbError) {
      console.error("Supabase DB Error:", dbError);
      throw new Error("Database error: " + dbError.message);
    }

    if (!entry || !entry.confirmation_token) {
      throw new Error("Failed to generate confirmation token");
    }

    // 2. Add to Brevo CRM (Contacts)
    try {
      const contactRes = await fetch("https://api.brevo.com/v3/contacts", {
        method: "POST",
        headers: {
          "api-key": BREVO_API_KEY,
          "Content-Type": "application/json",
          "accept": "application/json"
        },
        body: JSON.stringify({
          email: email,
          updateEnabled: true, // Update if exists
          listIds: [2] // Default list ID (usually #2 is first list), can be adjusted
        })
      });

      if (!contactRes.ok) {
        const errorText = await contactRes.text();
        console.error("BREVO_CRM_ERROR: Failed to create contact.", errorText);
        // Important: Check if List ID (default 2) exists in your Brevo account!
      } else {
        console.log("BREVO_CRM_SUCCESS: Contact created/updated.");
      }
    } catch (crmError) {
      console.error("Brevo CRM Error:", crmError);
    }

    // Construct DOI Link
    // Note: In local dev this might need adjustment, but for prod we use the project URL
    // We can extract project ref from SUPABASE_URL
    const projectUrl = SUPABASE_URL?.replace('.supabase.co', '.supabase.co/functions/v1');
    const confirmUrl = `${projectUrl}/confirm-doi?token=${entry.confirmation_token}`;

    // 3. Send Email via Brevo SMTP
    const emailHtml = `
<!DOCTYPE html>
<html>
<body style="font-family: sans-serif; line-height: 1.6; color: #1e293b; max-width: 600px; margin: 0 auto; padding: 20px;">
  <div style="background: white; border-radius: 12px; padding: 32px; border: 1px solid #e2e8f0;">
    <h2 style="color: #0f172a; margin-top: 0;">Bitte bestätigen Sie Ihre E-Mail</h2>
    <p>Vielen Dank für Ihr Interesse an der FlurPilot First-Mover Map.</p>
    <p>Um Missbrauch zu vermeiden, müssen wir sicherstellen, dass diese E-Mail Ihnen gehört. Klicken Sie auf den Button unten, um Ihre Adresse zu bestätigen und die Map zu erhalten.</p>
    
    <div style="text-align: center; margin: 32px 0;">
      <a href="${confirmUrl}" style="background-color: #059669; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">
        E-Mail bestätigen & Map laden
      </a>
    </div>

    <p style="font-size: 14px; color: #64748b;">
      Alternativ klicken Sie diesen Link: <br>
      <a href="${confirmUrl}" style="color: #059669;">${confirmUrl}</a>
    </p>

    <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 32px 0;">
    
    <p style="font-size: 12px; color: #94a3b8;">
      Sie erhalten diese E-Mail, weil Sie die FlurPilot Map angefordert haben. <br>
      FlurPilot • Stephan Ochmann • Emsdettener Straße 10 • 48268 Greven
    </p>
  </div>
</body>
</html>
    `;

    const emailResponse = await fetch("https://api.brevo.com/v3/smtp/email", {
      method: "POST",
      headers: {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json",
        "accept": "application/json"
      },
      body: JSON.stringify({
        sender: { name: "FlurPilot", email: "info@flurpilot.de" },
        to: [{ email: email }],
        subject: "Bitte bestätigen: Ihr Zugang zur First-Mover Map",
        htmlContent: emailHtml,
      }),
    });

    if (!emailResponse.ok) {
      const errorData = await emailResponse.text();
      console.error("Brevo API error:", errorData);
      throw new Error("Failed to send email via Brevo");
    }

    // Log analytics
    await supabase.from("analytics_events").insert({
      event_type: "doi_mail_sent_brevo",
      metadata: { source: "brevo_api" },
    });

    return new Response(
      JSON.stringify({ success: true, message: "Email sent via Brevo" }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );

  } catch (error: any) {
    console.error("Error:", error);
    return new Response(
      JSON.stringify({
        error: error.message || "Internal server error",
        message: error.message || "Internal server error"
      }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
