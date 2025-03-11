CREATE TABLE IF NOT EXISTS public.data (
    id character varying(32) PRIMARY KEY,
    profile character varying(32) NOT NULL,
    aristotelian_rhetoric character varying(32) NOT NULL,
    tone character varying(32) NOT NULL,
    approach character varying(32) NOT NULL,
    transcription text NULL,
    post_description text NULL,
    gemini_zs character varying(255) NULL,
    gemini_fs character varying(255) NULL,
    gemini_cot character varying(255) NULL,
    llama_zs character varying(255) NULL,
    llama_fs character varying(255) NULL,
    llama_cot character varying(255) NULL,
    deepseek_zs character varying(255) NULL,
    deepseek_fs character varying(255) NULL,
    deepseek_cot character varying(255) NULL
);