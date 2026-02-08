--
-- PostgreSQL database dump
--

\restrict b5B5LO05bTaP4In645hc01tzhOO2hDiIgVtreTSCt3SeR7cl8wOv8E6mDzdeOso

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: achievement; Type: TABLE; Schema: public; Owner: makson
--

CREATE TABLE public.achievement (
    id integer NOT NULL,
    stroke character varying(15) NOT NULL,
    "time" time with time zone NOT NULL,
    distance_meters integer NOT NULL,
    competition_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.achievement OWNER TO makson;

--
-- Name: achievement_id_seq; Type: SEQUENCE; Schema: public; Owner: makson
--

CREATE SEQUENCE public.achievement_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.achievement_id_seq OWNER TO makson;

--
-- Name: achievement_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: makson
--

ALTER SEQUENCE public.achievement_id_seq OWNED BY public.achievement.id;


--
-- Name: activity; Type: TABLE; Schema: public; Owner: makson
--

CREATE TABLE public.activity (
    id integer NOT NULL,
    day timestamp with time zone NOT NULL,
    stroke character varying(15) NOT NULL,
    distance_meters integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.activity OWNER TO makson;

--
-- Name: activity_id_seq; Type: SEQUENCE; Schema: public; Owner: makson
--

CREATE SEQUENCE public.activity_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.activity_id_seq OWNER TO makson;

--
-- Name: activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: makson
--

ALTER SEQUENCE public.activity_id_seq OWNED BY public.activity.id;


--
-- Name: competition; Type: TABLE; Schema: public; Owner: makson
--

CREATE TABLE public.competition (
    id integer NOT NULL,
    name character varying(25) NOT NULL,
    location character varying(100) NOT NULL,
    date date
);


ALTER TABLE public.competition OWNER TO makson;

--
-- Name: competition_id_seq; Type: SEQUENCE; Schema: public; Owner: makson
--

CREATE SEQUENCE public.competition_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.competition_id_seq OWNER TO makson;

--
-- Name: competition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: makson
--

ALTER SEQUENCE public.competition_id_seq OWNED BY public.competition.id;


--
-- Name: equipment; Type: TABLE; Schema: public; Owner: makson
--

CREATE TABLE public.equipment (
    id integer NOT NULL,
    name character varying(20),
    typ character varying(15),
    brand character varying(25),
    achievement_id integer NOT NULL
);


ALTER TABLE public.equipment OWNER TO makson;

--
-- Name: equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: makson
--

CREATE SEQUENCE public.equipment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.equipment_id_seq OWNER TO makson;

--
-- Name: equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: makson
--

ALTER SEQUENCE public.equipment_id_seq OWNED BY public.equipment.id;


--
-- Name: goal; Type: TABLE; Schema: public; Owner: makson
--

CREATE TABLE public.goal (
    id integer NOT NULL,
    target_distance integer NOT NULL,
    deadline date NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.goal OWNER TO makson;

--
-- Name: goal_id_seq; Type: SEQUENCE; Schema: public; Owner: makson
--

CREATE SEQUENCE public.goal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.goal_id_seq OWNER TO makson;

--
-- Name: goal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: makson
--

ALTER SEQUENCE public.goal_id_seq OWNED BY public.goal.id;


--
-- Name: rating; Type: TABLE; Schema: public; Owner: makson
--

CREATE TABLE public.rating (
    id integer NOT NULL,
    created_at timestamp without time zone NOT NULL,
    value integer NOT NULL,
    user_id integer NOT NULL,
    achievement_id integer NOT NULL
);


ALTER TABLE public.rating OWNER TO makson;

--
-- Name: rating_id_seq; Type: SEQUENCE; Schema: public; Owner: makson
--

CREATE SEQUENCE public.rating_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.rating_id_seq OWNER TO makson;

--
-- Name: rating_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: makson
--

ALTER SEQUENCE public.rating_id_seq OWNED BY public.rating.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: makson
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    email character varying(40) NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    age integer,
    password_hash character varying(256) NOT NULL
);


ALTER TABLE public."user" OWNER TO makson;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: makson
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO makson;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: makson
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: achievement id; Type: DEFAULT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.achievement ALTER COLUMN id SET DEFAULT nextval('public.achievement_id_seq'::regclass);


--
-- Name: activity id; Type: DEFAULT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.activity ALTER COLUMN id SET DEFAULT nextval('public.activity_id_seq'::regclass);


--
-- Name: competition id; Type: DEFAULT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.competition ALTER COLUMN id SET DEFAULT nextval('public.competition_id_seq'::regclass);


--
-- Name: equipment id; Type: DEFAULT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.equipment ALTER COLUMN id SET DEFAULT nextval('public.equipment_id_seq'::regclass);


--
-- Name: goal id; Type: DEFAULT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.goal ALTER COLUMN id SET DEFAULT nextval('public.goal_id_seq'::regclass);


--
-- Name: rating id; Type: DEFAULT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.rating ALTER COLUMN id SET DEFAULT nextval('public.rating_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: achievement achievement_pkey; Type: CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.achievement
    ADD CONSTRAINT achievement_pkey PRIMARY KEY (id);


--
-- Name: activity activity_pkey; Type: CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_pkey PRIMARY KEY (id);


--
-- Name: competition competition_pkey; Type: CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.competition
    ADD CONSTRAINT competition_pkey PRIMARY KEY (id);


--
-- Name: equipment equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_pkey PRIMARY KEY (id);


--
-- Name: goal goal_pkey; Type: CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.goal
    ADD CONSTRAINT goal_pkey PRIMARY KEY (id);


--
-- Name: rating rating_pkey; Type: CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_pkey PRIMARY KEY (id);


--
-- Name: user uq_user_email; Type: CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT uq_user_email UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: achievement achievement_competition_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.achievement
    ADD CONSTRAINT achievement_competition_id_fkey FOREIGN KEY (competition_id) REFERENCES public.competition(id);


--
-- Name: achievement achievement_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.achievement
    ADD CONSTRAINT achievement_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: activity activity_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.activity
    ADD CONSTRAINT activity_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: equipment equipment_achievement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.equipment
    ADD CONSTRAINT equipment_achievement_id_fkey FOREIGN KEY (achievement_id) REFERENCES public.achievement(id);


--
-- Name: goal goal_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.goal
    ADD CONSTRAINT goal_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: rating rating_achievement_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_achievement_id_fkey FOREIGN KEY (achievement_id) REFERENCES public.achievement(id);


--
-- Name: rating rating_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: makson
--

ALTER TABLE ONLY public.rating
    ADD CONSTRAINT rating_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

\unrestrict b5B5LO05bTaP4In645hc01tzhOO2hDiIgVtreTSCt3SeR7cl8wOv8E6mDzdeOso

