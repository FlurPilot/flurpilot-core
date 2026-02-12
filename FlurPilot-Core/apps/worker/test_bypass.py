from unittest.mock import MagicMock
from bavarian_bypass import BavarianBypass

def test_bypass_mock():
    print("Testing Bavarian Bypass (Mock)...")
    
    # Mock Supabase Client
    mock_supabase = MagicMock()
    mock_rpc = MagicMock()
    mock_supabase.rpc.return_value = mock_rpc
    mock_rpc.execute.return_value.data = "uuid-1234-virtual-parcel"
    
    engine = BavarianBypass(mock_supabase)
    
    field_id = "field-abc-123"
    result_id = engine.process_field(field_id)
    
    # Verify RPC call
    mock_supabase.rpc.assert_called_with("calculate_virtual_parcel", {"field_block_id": field_id})
    
    if result_id == "uuid-1234-virtual-parcel":
        print("✅ Mock RPC Call Successful.")
    else:
        print("❌ MockRPC Call Failed.")

if __name__ == "__main__":
    test_bypass_mock()
