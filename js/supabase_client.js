// js/supabase_client.js
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

const SUPABASE_URL = 'https://ubvoznyoughnwsmqdafl.supabase.co'
const SUPABASE_KEY = 'sb_publishable_0-2AAqmJh53z1jGsx3-gpQ_YCdejYdI'

export const supabase = createClient(SUPABASE_URL, SUPABASE_KEY)
