SET client_encoding = 'UTF8';

CREATE TABLE public.pages (
    id integer NOT NULL,
    slug character varying(150) NOT NULL,
    time_c timestamp without time zone NOT NULL,
    time_m timestamp without time zone NOT NULL,
    user_id_c integer NOT NULL,
    user_id_m integer NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    style character varying(64) NOT NULL
);

CREATE SEQUENCE public.pages_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;

ALTER SEQUENCE public.pages_id_seq OWNED BY public.pages.id;

CREATE TABLE public.settings (
    module character(24) NOT NULL,
    status character(7) NOT NULL,
    name character(24) NOT NULL,
    value text NOT NULL
);

CREATE TABLE public.users (
    id integer NOT NULL,
    uname character(32) NOT NULL,
    pwd character(32) NOT NULL,
    name character varying(64) NOT NULL
);

CREATE SEQUENCE public.users_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;

CREATE TABLE public.weblog (
    id integer NOT NULL,
    title character varying(255) NOT NULL,
    link character varying(511),
    via character varying(511),
    time_c timestamp without time zone NOT NULL,
    time_m timestamp without time zone NOT NULL,
    user_id_c integer NOT NULL,
    user_id_m integer NOT NULL,
    note text NOT NULL
);

CREATE SEQUENCE public.weblog_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;

ALTER TABLE public.weblog_id_seq OWNER TO keith;

ALTER SEQUENCE public.weblog_id_seq OWNED BY public.weblog.id;

ALTER TABLE ONLY public.pages ALTER COLUMN id SET DEFAULT nextval('public.pages_id_seq'::regclass);

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);

ALTER TABLE ONLY public.weblog ALTER COLUMN id SET DEFAULT nextval('public.weblog_id_seq'::regclass);

ALTER TABLE ONLY public.output_cache ADD CONSTRAINT output_cache_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.pages ADD CONSTRAINT pages_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.pages ADD CONSTRAINT pages_slug_key UNIQUE (slug);

ALTER TABLE ONLY public.settings ADD CONSTRAINT settings_pkey PRIMARY KEY (module, status, name);

ALTER TABLE ONLY public.users ADD CONSTRAINT users_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.users ADD CONSTRAINT users_uname_key UNIQUE (uname);

ALTER TABLE ONLY public.weblog ADD CONSTRAINT weblog_link_key UNIQUE (link);

ALTER TABLE ONLY public.weblog ADD CONSTRAINT weblog_pkey PRIMARY KEY (id);

CREATE INDEX output_cache_timestamp ON public.output_cache USING btree (ts);

CREATE INDEX pages_created ON public.pages USING btree (time_c);

CREATE INDEX weblog_created ON public.weblog USING btree (time_c);

CREATE INDEX weblog_modified ON public.weblog USING btree (time_m);

ALTER TABLE ONLY public.pages ADD CONSTRAINT pages_user_id_c_fkey FOREIGN KEY (user_id_c) REFERENCES public.users(id);

ALTER TABLE ONLY public.pages ADD CONSTRAINT pages_user_id_m_fkey FOREIGN KEY (user_id_m) REFERENCES public.users(id);

ALTER TABLE ONLY public.weblog ADD CONSTRAINT weblog_user_id_c_fkey FOREIGN KEY (user_id_c) REFERENCES public.users(id);

ALTER TABLE ONLY public.weblog ADD CONSTRAINT weblog_user_id_m_fkey FOREIGN KEY (user_id_m) REFERENCES public.users(id);
