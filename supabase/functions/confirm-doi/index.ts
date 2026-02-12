// Supabase Edge Function: confirm-doi
// Deploy with: supabase functions deploy confirm-doi

import { serve } from "https://deno.land/std@0.177.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL");
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
// Optional: Redirect to a specific "Thank You" page or the PDF directly
// For MVP, we'll redirect to a simple success page or the landing page with a query param
const SITE_URL = Deno.env.get("SITE_URL") || "https://flurpilot.de";

serve(async (req) => {
  try {
    const url = new URL(req.url);
    const token = url.searchParams.get("token");

    if (!token) {
      return new Response("Missing token", { status: 400 });
    }

    const supabase = createClient(SUPABASE_URL!, SUPABASE_SERVICE_ROLE_KEY!);

    // 1. Verify Token
    const { data: entry, error } = await supabase
      .from("waitlist")
      .select("*")
      .eq("confirmation_token", token)
      .single();

    if (error) {
      console.error("DB Query Error:", error);
      return new Response("Database Error: " + error.message, { status: 500 });
    }

    if (!entry) {
      return new Response("Invalid or expired token", { status: 400 });
    }

    // 2. Update Status
    const { error: updateError } = await supabase
      .from("waitlist")
      .update({
        status: 'confirmed',
        confirmed_at: new Date().toISOString(),
        signup_ip: req.headers.get("x-forwarded-for") || "unknown"
      })
      .eq("id", entry.id);

    if (updateError) {
      console.error("Update Error", updateError);
      return new Response("Database error", { status: 500 });
    }

    // 3. Log Event
    await supabase.from("analytics_events").insert({
      event_type: "doi_confirmed",
      metadata: { waitlist_id: entry.id }
    });

    // 4. Redirect to Success Page (User gets the Freebie there)
    // We append ?confirmed=true so the frontend can react (e.g. auto-download)
    return Response.redirect(`${SITE_URL}/?confirmed=true`, 302);

  } catch (error) {
    console.error("Error:", error);
    return new Response("Internal Server Error", { status: 500 });
  }
});
