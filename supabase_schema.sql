-- Sefarad-MX: Webtrees-style Genealogical Schema

-- 1. Individuals (INDI)
CREATE TABLE IF NOT EXISTS individuals (
  id TEXT PRIMARY KEY, -- GEDCOM ID e.g., @I1@
  full_name TEXT NOT NULL,
  first_name TEXT,
  last_name TEXT,
  gender CHAR(1),
  birth_date TEXT,
  birth_place TEXT,
  death_date TEXT,
  death_place TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 2. Families (FAM)
CREATE TABLE IF NOT EXISTS families (
  id TEXT PRIMARY KEY, -- GEDCOM ID e.g., @F1@
  husband_id TEXT REFERENCES individuals(id),
  wife_id TEXT REFERENCES individuals(id),
  marriage_date TEXT,
  marriage_place TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 3. Family Children (Linking FAM to INDI)
CREATE TABLE IF NOT EXISTS family_children (
  family_id TEXT REFERENCES families(id) ON DELETE CASCADE,
  child_id TEXT REFERENCES individuals(id) ON DELETE CASCADE,
  PRIMARY KEY (family_id, child_id)
);

-- 4. Sources (SOUR)
CREATE TABLE IF NOT EXISTS sources (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  gedcom_id TEXT, -- e.g., @S1@
  title TEXT NOT NULL,
  author TEXT,
  publication_info TEXT,
  repository TEXT,
  metadata JSONB DEFAULT '{}'::jsonb
);

-- 5. Media (OBJE)
CREATE TABLE IF NOT EXISTS media (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  file_name TEXT NOT NULL,
  file_url TEXT, -- URL in Supabase Storage or external
  file_type TEXT,
  title TEXT,
  metadata JSONB DEFAULT '{}'::jsonb
);

-- 6. Citations & Transcriptions (The "Webtrees" core)
CREATE TABLE IF NOT EXISTS citations (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  individual_id TEXT REFERENCES individuals(id) ON DELETE CASCADE,
  family_id TEXT REFERENCES families(id) ON DELETE CASCADE,
  source_id UUID REFERENCES sources(id) ON DELETE SET NULL,
  media_id UUID REFERENCES media(id) ON DELETE SET NULL,
  page TEXT,
  transcription TEXT, -- Full text from .txt files
  confidence_level INTEGER DEFAULT 3, -- 0-3
  note TEXT,
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Enable Search
CREATE INDEX IF NOT EXISTS idx_indis_name ON individuals USING gin (full_name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_citations_transcription ON citations USING gin (to_tsvector('spanish', transcription));
