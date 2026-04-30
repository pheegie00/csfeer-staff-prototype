--
-- PostgreSQL database dump
--

\restrict 01S3XTiIxztxGy9rZLcdd5kYk9Ybqh6QJzEnZOeBpEEo2P4PyYRRjWUVDqSAur4

-- Dumped from database version 16.13 (Debian 16.13-1.pgdg13+1)
-- Dumped by pg_dump version 16.13 (Debian 16.13-1.pgdg13+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: csfeerauth; Type: DATABASE; Schema: -; Owner: csfeer
--

CREATE DATABASE csfeerauth WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.utf8';


ALTER DATABASE csfeerauth OWNER TO csfeer;

\unrestrict 01S3XTiIxztxGy9rZLcdd5kYk9Ybqh6QJzEnZOeBpEEo2P4PyYRRjWUVDqSAur4
\connect csfeerauth
\restrict 01S3XTiIxztxGy9rZLcdd5kYk9Ybqh6QJzEnZOeBpEEo2P4PyYRRjWUVDqSAur4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
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
-- Name: admin_event_entity; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.admin_event_entity (
    id character varying(36) NOT NULL,
    admin_event_time bigint,
    realm_id character varying(255),
    operation_type character varying(255),
    auth_realm_id character varying(255),
    auth_client_id character varying(255),
    auth_user_id character varying(255),
    ip_address character varying(255),
    resource_path character varying(2550),
    representation text,
    error character varying(255),
    resource_type character varying(64),
    details_json text
);


ALTER TABLE public.admin_event_entity OWNER TO csfeer;

--
-- Name: associated_policy; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.associated_policy (
    policy_id character varying(36) NOT NULL,
    associated_policy_id character varying(36) NOT NULL
);


ALTER TABLE public.associated_policy OWNER TO csfeer;

--
-- Name: authentication_execution; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.authentication_execution (
    id character varying(36) NOT NULL,
    alias character varying(255),
    authenticator character varying(36),
    realm_id character varying(36),
    flow_id character varying(36),
    requirement integer,
    priority integer,
    authenticator_flow boolean DEFAULT false NOT NULL,
    auth_flow_id character varying(36),
    auth_config character varying(36)
);


ALTER TABLE public.authentication_execution OWNER TO csfeer;

--
-- Name: authentication_flow; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.authentication_flow (
    id character varying(36) NOT NULL,
    alias character varying(255),
    description character varying(255),
    realm_id character varying(36),
    provider_id character varying(36) DEFAULT 'basic-flow'::character varying NOT NULL,
    top_level boolean DEFAULT false NOT NULL,
    built_in boolean DEFAULT false NOT NULL
);


ALTER TABLE public.authentication_flow OWNER TO csfeer;

--
-- Name: authenticator_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.authenticator_config (
    id character varying(36) NOT NULL,
    alias character varying(255),
    realm_id character varying(36)
);


ALTER TABLE public.authenticator_config OWNER TO csfeer;

--
-- Name: authenticator_config_entry; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.authenticator_config_entry (
    authenticator_id character varying(36) NOT NULL,
    value text,
    name character varying(255) NOT NULL
);


ALTER TABLE public.authenticator_config_entry OWNER TO csfeer;

--
-- Name: broker_link; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.broker_link (
    identity_provider character varying(255) NOT NULL,
    storage_provider_id character varying(255),
    realm_id character varying(36) NOT NULL,
    broker_user_id character varying(255),
    broker_username character varying(255),
    token text,
    user_id character varying(255) NOT NULL
);


ALTER TABLE public.broker_link OWNER TO csfeer;

--
-- Name: client; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client (
    id character varying(36) NOT NULL,
    enabled boolean DEFAULT false NOT NULL,
    full_scope_allowed boolean DEFAULT false NOT NULL,
    client_id character varying(255),
    not_before integer,
    public_client boolean DEFAULT false NOT NULL,
    secret character varying(255),
    base_url character varying(255),
    bearer_only boolean DEFAULT false NOT NULL,
    management_url character varying(255),
    surrogate_auth_required boolean DEFAULT false NOT NULL,
    realm_id character varying(36),
    protocol character varying(255),
    node_rereg_timeout integer DEFAULT 0,
    frontchannel_logout boolean DEFAULT false NOT NULL,
    consent_required boolean DEFAULT false NOT NULL,
    name character varying(255),
    service_accounts_enabled boolean DEFAULT false NOT NULL,
    client_authenticator_type character varying(255),
    root_url character varying(255),
    description character varying(255),
    registration_token character varying(255),
    standard_flow_enabled boolean DEFAULT true NOT NULL,
    implicit_flow_enabled boolean DEFAULT false NOT NULL,
    direct_access_grants_enabled boolean DEFAULT false NOT NULL,
    always_display_in_console boolean DEFAULT false NOT NULL
);


ALTER TABLE public.client OWNER TO csfeer;

--
-- Name: client_attributes; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client_attributes (
    client_id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    value text
);


ALTER TABLE public.client_attributes OWNER TO csfeer;

--
-- Name: client_auth_flow_bindings; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client_auth_flow_bindings (
    client_id character varying(36) NOT NULL,
    flow_id character varying(36),
    binding_name character varying(255) NOT NULL
);


ALTER TABLE public.client_auth_flow_bindings OWNER TO csfeer;

--
-- Name: client_initial_access; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client_initial_access (
    id character varying(36) NOT NULL,
    realm_id character varying(36) NOT NULL,
    "timestamp" integer,
    expiration integer,
    count integer,
    remaining_count integer
);


ALTER TABLE public.client_initial_access OWNER TO csfeer;

--
-- Name: client_node_registrations; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client_node_registrations (
    client_id character varying(36) NOT NULL,
    value integer,
    name character varying(255) NOT NULL
);


ALTER TABLE public.client_node_registrations OWNER TO csfeer;

--
-- Name: client_scope; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client_scope (
    id character varying(36) NOT NULL,
    name character varying(255),
    realm_id character varying(36),
    description character varying(255),
    protocol character varying(255)
);


ALTER TABLE public.client_scope OWNER TO csfeer;

--
-- Name: client_scope_attributes; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client_scope_attributes (
    scope_id character varying(36) NOT NULL,
    value character varying(2048),
    name character varying(255) NOT NULL
);


ALTER TABLE public.client_scope_attributes OWNER TO csfeer;

--
-- Name: client_scope_client; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client_scope_client (
    client_id character varying(255) NOT NULL,
    scope_id character varying(255) NOT NULL,
    default_scope boolean DEFAULT false NOT NULL
);


ALTER TABLE public.client_scope_client OWNER TO csfeer;

--
-- Name: client_scope_role_mapping; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.client_scope_role_mapping (
    scope_id character varying(36) NOT NULL,
    role_id character varying(36) NOT NULL
);


ALTER TABLE public.client_scope_role_mapping OWNER TO csfeer;

--
-- Name: component; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.component (
    id character varying(36) NOT NULL,
    name character varying(255),
    parent_id character varying(36),
    provider_id character varying(36),
    provider_type character varying(255),
    realm_id character varying(36),
    sub_type character varying(255)
);


ALTER TABLE public.component OWNER TO csfeer;

--
-- Name: component_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.component_config (
    id character varying(36) NOT NULL,
    component_id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    value text
);


ALTER TABLE public.component_config OWNER TO csfeer;

--
-- Name: composite_role; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.composite_role (
    composite character varying(36) NOT NULL,
    child_role character varying(36) NOT NULL
);


ALTER TABLE public.composite_role OWNER TO csfeer;

--
-- Name: credential; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.credential (
    id character varying(36) NOT NULL,
    salt bytea,
    type character varying(255),
    user_id character varying(36),
    created_date bigint,
    user_label character varying(255),
    secret_data text,
    credential_data text,
    priority integer,
    version integer DEFAULT 0
);


ALTER TABLE public.credential OWNER TO csfeer;

--
-- Name: databasechangelog; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.databasechangelog (
    id character varying(255) NOT NULL,
    author character varying(255) NOT NULL,
    filename character varying(255) NOT NULL,
    dateexecuted timestamp without time zone NOT NULL,
    orderexecuted integer NOT NULL,
    exectype character varying(10) NOT NULL,
    md5sum character varying(35),
    description character varying(255),
    comments character varying(255),
    tag character varying(255),
    liquibase character varying(20),
    contexts character varying(255),
    labels character varying(255),
    deployment_id character varying(10)
);


ALTER TABLE public.databasechangelog OWNER TO csfeer;

--
-- Name: databasechangeloglock; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.databasechangeloglock (
    id integer NOT NULL,
    locked boolean NOT NULL,
    lockgranted timestamp without time zone,
    lockedby character varying(255)
);


ALTER TABLE public.databasechangeloglock OWNER TO csfeer;

--
-- Name: default_client_scope; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.default_client_scope (
    realm_id character varying(36) NOT NULL,
    scope_id character varying(36) NOT NULL,
    default_scope boolean DEFAULT false NOT NULL
);


ALTER TABLE public.default_client_scope OWNER TO csfeer;

--
-- Name: event_entity; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.event_entity (
    id character varying(36) NOT NULL,
    client_id character varying(255),
    details_json character varying(2550),
    error character varying(255),
    ip_address character varying(255),
    realm_id character varying(255),
    session_id character varying(255),
    event_time bigint,
    type character varying(255),
    user_id character varying(255),
    details_json_long_value text
);


ALTER TABLE public.event_entity OWNER TO csfeer;

--
-- Name: fed_user_attribute; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.fed_user_attribute (
    id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    user_id character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL,
    storage_provider_id character varying(36),
    value character varying(2024),
    long_value_hash bytea,
    long_value_hash_lower_case bytea,
    long_value text
);


ALTER TABLE public.fed_user_attribute OWNER TO csfeer;

--
-- Name: fed_user_consent; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.fed_user_consent (
    id character varying(36) NOT NULL,
    client_id character varying(255),
    user_id character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL,
    storage_provider_id character varying(36),
    created_date bigint,
    last_updated_date bigint,
    client_storage_provider character varying(36),
    external_client_id character varying(255)
);


ALTER TABLE public.fed_user_consent OWNER TO csfeer;

--
-- Name: fed_user_consent_cl_scope; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.fed_user_consent_cl_scope (
    user_consent_id character varying(36) NOT NULL,
    scope_id character varying(36) NOT NULL
);


ALTER TABLE public.fed_user_consent_cl_scope OWNER TO csfeer;

--
-- Name: fed_user_credential; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.fed_user_credential (
    id character varying(36) NOT NULL,
    salt bytea,
    type character varying(255),
    created_date bigint,
    user_id character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL,
    storage_provider_id character varying(36),
    user_label character varying(255),
    secret_data text,
    credential_data text,
    priority integer
);


ALTER TABLE public.fed_user_credential OWNER TO csfeer;

--
-- Name: fed_user_group_membership; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.fed_user_group_membership (
    group_id character varying(36) NOT NULL,
    user_id character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL,
    storage_provider_id character varying(36)
);


ALTER TABLE public.fed_user_group_membership OWNER TO csfeer;

--
-- Name: fed_user_required_action; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.fed_user_required_action (
    required_action character varying(255) DEFAULT ' '::character varying NOT NULL,
    user_id character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL,
    storage_provider_id character varying(36)
);


ALTER TABLE public.fed_user_required_action OWNER TO csfeer;

--
-- Name: fed_user_role_mapping; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.fed_user_role_mapping (
    role_id character varying(36) NOT NULL,
    user_id character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL,
    storage_provider_id character varying(36)
);


ALTER TABLE public.fed_user_role_mapping OWNER TO csfeer;

--
-- Name: federated_identity; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.federated_identity (
    identity_provider character varying(255) NOT NULL,
    realm_id character varying(36),
    federated_user_id character varying(255),
    federated_username character varying(255),
    token text,
    user_id character varying(36) NOT NULL
);


ALTER TABLE public.federated_identity OWNER TO csfeer;

--
-- Name: federated_user; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.federated_user (
    id character varying(255) NOT NULL,
    storage_provider_id character varying(255),
    realm_id character varying(36) NOT NULL
);


ALTER TABLE public.federated_user OWNER TO csfeer;

--
-- Name: group_attribute; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.group_attribute (
    id character varying(36) DEFAULT 'sybase-needs-something-here'::character varying NOT NULL,
    name character varying(255) NOT NULL,
    value character varying(255),
    group_id character varying(36) NOT NULL
);


ALTER TABLE public.group_attribute OWNER TO csfeer;

--
-- Name: group_role_mapping; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.group_role_mapping (
    role_id character varying(36) NOT NULL,
    group_id character varying(36) NOT NULL
);


ALTER TABLE public.group_role_mapping OWNER TO csfeer;

--
-- Name: identity_provider; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.identity_provider (
    internal_id character varying(36) NOT NULL,
    enabled boolean DEFAULT false NOT NULL,
    provider_alias character varying(255),
    provider_id character varying(255),
    store_token boolean,
    authenticate_by_default boolean,
    realm_id character varying(36),
    add_token_role boolean,
    trust_email boolean,
    first_broker_login_flow_id character varying(36),
    post_broker_login_flow_id character varying(36),
    provider_display_name character varying(255),
    link_only boolean,
    organization_id character varying(255),
    hide_on_login boolean
);


ALTER TABLE public.identity_provider OWNER TO csfeer;

--
-- Name: identity_provider_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.identity_provider_config (
    identity_provider_id character varying(36) NOT NULL,
    value text,
    name character varying(255) NOT NULL
);


ALTER TABLE public.identity_provider_config OWNER TO csfeer;

--
-- Name: identity_provider_mapper; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.identity_provider_mapper (
    id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    idp_alias character varying(255) NOT NULL,
    idp_mapper_name character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL
);


ALTER TABLE public.identity_provider_mapper OWNER TO csfeer;

--
-- Name: idp_mapper_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.idp_mapper_config (
    idp_mapper_id character varying(36) NOT NULL,
    value text,
    name character varying(255) NOT NULL
);


ALTER TABLE public.idp_mapper_config OWNER TO csfeer;

--
-- Name: jgroups_ping; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.jgroups_ping (
    address character varying(200) NOT NULL,
    name character varying(200),
    cluster_name character varying(200) NOT NULL,
    ip character varying(200) NOT NULL,
    coord boolean
);


ALTER TABLE public.jgroups_ping OWNER TO csfeer;

--
-- Name: keycloak_group; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.keycloak_group (
    id character varying(36) NOT NULL,
    name character varying(255),
    parent_group character varying(36) NOT NULL,
    realm_id character varying(36),
    type integer DEFAULT 0 NOT NULL,
    description character varying(255)
);


ALTER TABLE public.keycloak_group OWNER TO csfeer;

--
-- Name: keycloak_role; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.keycloak_role (
    id character varying(36) NOT NULL,
    client_realm_constraint character varying(255),
    client_role boolean DEFAULT false NOT NULL,
    description character varying(255),
    name character varying(255),
    realm_id character varying(255),
    client character varying(36),
    realm character varying(36)
);


ALTER TABLE public.keycloak_role OWNER TO csfeer;

--
-- Name: migration_model; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.migration_model (
    id character varying(36) NOT NULL,
    version character varying(36),
    update_time bigint DEFAULT 0 NOT NULL
);


ALTER TABLE public.migration_model OWNER TO csfeer;

--
-- Name: offline_client_session; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.offline_client_session (
    user_session_id character varying(36) NOT NULL,
    client_id character varying(255) NOT NULL,
    offline_flag character varying(4) NOT NULL,
    "timestamp" integer,
    data text,
    client_storage_provider character varying(36) DEFAULT 'local'::character varying NOT NULL,
    external_client_id character varying(255) DEFAULT 'local'::character varying NOT NULL,
    version integer DEFAULT 0
);


ALTER TABLE public.offline_client_session OWNER TO csfeer;

--
-- Name: offline_user_session; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.offline_user_session (
    user_session_id character varying(36) NOT NULL,
    user_id character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL,
    created_on integer NOT NULL,
    offline_flag character varying(4) NOT NULL,
    data text,
    last_session_refresh integer DEFAULT 0 NOT NULL,
    broker_session_id character varying(1024),
    version integer DEFAULT 0,
    remember_me boolean
);


ALTER TABLE public.offline_user_session OWNER TO csfeer;

--
-- Name: org; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.org (
    id character varying(255) NOT NULL,
    enabled boolean NOT NULL,
    realm_id character varying(255) NOT NULL,
    group_id character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(4000),
    alias character varying(255) NOT NULL,
    redirect_url character varying(2048)
);


ALTER TABLE public.org OWNER TO csfeer;

--
-- Name: org_domain; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.org_domain (
    id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    verified boolean NOT NULL,
    org_id character varying(255) NOT NULL
);


ALTER TABLE public.org_domain OWNER TO csfeer;

--
-- Name: org_invitation; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.org_invitation (
    id character varying(36) NOT NULL,
    organization_id character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    first_name character varying(255),
    last_name character varying(255),
    created_at integer NOT NULL,
    expires_at integer,
    invite_link character varying(2048)
);


ALTER TABLE public.org_invitation OWNER TO csfeer;

--
-- Name: policy_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.policy_config (
    policy_id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    value text
);


ALTER TABLE public.policy_config OWNER TO csfeer;

--
-- Name: protocol_mapper; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.protocol_mapper (
    id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    protocol character varying(255) NOT NULL,
    protocol_mapper_name character varying(255) NOT NULL,
    client_id character varying(36),
    client_scope_id character varying(36)
);


ALTER TABLE public.protocol_mapper OWNER TO csfeer;

--
-- Name: protocol_mapper_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.protocol_mapper_config (
    protocol_mapper_id character varying(36) NOT NULL,
    value text,
    name character varying(255) NOT NULL
);


ALTER TABLE public.protocol_mapper_config OWNER TO csfeer;

--
-- Name: realm; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm (
    id character varying(36) NOT NULL,
    access_code_lifespan integer,
    user_action_lifespan integer,
    access_token_lifespan integer,
    account_theme character varying(255),
    admin_theme character varying(255),
    email_theme character varying(255),
    enabled boolean DEFAULT false NOT NULL,
    events_enabled boolean DEFAULT false NOT NULL,
    events_expiration bigint,
    login_theme character varying(255),
    name character varying(255),
    not_before integer,
    password_policy character varying(2550),
    registration_allowed boolean DEFAULT false NOT NULL,
    remember_me boolean DEFAULT false NOT NULL,
    reset_password_allowed boolean DEFAULT false NOT NULL,
    social boolean DEFAULT false NOT NULL,
    ssl_required character varying(255),
    sso_idle_timeout integer,
    sso_max_lifespan integer,
    update_profile_on_soc_login boolean DEFAULT false NOT NULL,
    verify_email boolean DEFAULT false NOT NULL,
    master_admin_client character varying(36),
    login_lifespan integer,
    internationalization_enabled boolean DEFAULT false NOT NULL,
    default_locale character varying(255),
    reg_email_as_username boolean DEFAULT false NOT NULL,
    admin_events_enabled boolean DEFAULT false NOT NULL,
    admin_events_details_enabled boolean DEFAULT false NOT NULL,
    edit_username_allowed boolean DEFAULT false NOT NULL,
    otp_policy_counter integer DEFAULT 0,
    otp_policy_window integer DEFAULT 1,
    otp_policy_period integer DEFAULT 30,
    otp_policy_digits integer DEFAULT 6,
    otp_policy_alg character varying(36) DEFAULT 'HmacSHA1'::character varying,
    otp_policy_type character varying(36) DEFAULT 'totp'::character varying,
    browser_flow character varying(36),
    registration_flow character varying(36),
    direct_grant_flow character varying(36),
    reset_credentials_flow character varying(36),
    client_auth_flow character varying(36),
    offline_session_idle_timeout integer DEFAULT 0,
    revoke_refresh_token boolean DEFAULT false NOT NULL,
    access_token_life_implicit integer DEFAULT 0,
    login_with_email_allowed boolean DEFAULT true NOT NULL,
    duplicate_emails_allowed boolean DEFAULT false NOT NULL,
    docker_auth_flow character varying(36),
    refresh_token_max_reuse integer DEFAULT 0,
    allow_user_managed_access boolean DEFAULT false NOT NULL,
    sso_max_lifespan_remember_me integer DEFAULT 0 NOT NULL,
    sso_idle_timeout_remember_me integer DEFAULT 0 NOT NULL,
    default_role character varying(255)
);


ALTER TABLE public.realm OWNER TO csfeer;

--
-- Name: realm_attribute; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm_attribute (
    name character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL,
    value text
);


ALTER TABLE public.realm_attribute OWNER TO csfeer;

--
-- Name: realm_default_groups; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm_default_groups (
    realm_id character varying(36) NOT NULL,
    group_id character varying(36) NOT NULL
);


ALTER TABLE public.realm_default_groups OWNER TO csfeer;

--
-- Name: realm_enabled_event_types; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm_enabled_event_types (
    realm_id character varying(36) NOT NULL,
    value character varying(255) NOT NULL
);


ALTER TABLE public.realm_enabled_event_types OWNER TO csfeer;

--
-- Name: realm_events_listeners; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm_events_listeners (
    realm_id character varying(36) NOT NULL,
    value character varying(255) NOT NULL
);


ALTER TABLE public.realm_events_listeners OWNER TO csfeer;

--
-- Name: realm_localizations; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm_localizations (
    realm_id character varying(255) NOT NULL,
    locale character varying(255) NOT NULL,
    texts text NOT NULL
);


ALTER TABLE public.realm_localizations OWNER TO csfeer;

--
-- Name: realm_required_credential; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm_required_credential (
    type character varying(255) NOT NULL,
    form_label character varying(255),
    input boolean DEFAULT false NOT NULL,
    secret boolean DEFAULT false NOT NULL,
    realm_id character varying(36) NOT NULL
);


ALTER TABLE public.realm_required_credential OWNER TO csfeer;

--
-- Name: realm_smtp_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm_smtp_config (
    realm_id character varying(36) NOT NULL,
    value character varying(255),
    name character varying(255) NOT NULL
);


ALTER TABLE public.realm_smtp_config OWNER TO csfeer;

--
-- Name: realm_supported_locales; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.realm_supported_locales (
    realm_id character varying(36) NOT NULL,
    value character varying(255) NOT NULL
);


ALTER TABLE public.realm_supported_locales OWNER TO csfeer;

--
-- Name: redirect_uris; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.redirect_uris (
    client_id character varying(36) NOT NULL,
    value character varying(255) NOT NULL
);


ALTER TABLE public.redirect_uris OWNER TO csfeer;

--
-- Name: required_action_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.required_action_config (
    required_action_id character varying(36) NOT NULL,
    value text,
    name character varying(255) NOT NULL
);


ALTER TABLE public.required_action_config OWNER TO csfeer;

--
-- Name: required_action_provider; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.required_action_provider (
    id character varying(36) NOT NULL,
    alias character varying(255),
    name character varying(255),
    realm_id character varying(36),
    enabled boolean DEFAULT false NOT NULL,
    default_action boolean DEFAULT false NOT NULL,
    provider_id character varying(255),
    priority integer
);


ALTER TABLE public.required_action_provider OWNER TO csfeer;

--
-- Name: resource_attribute; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_attribute (
    id character varying(36) DEFAULT 'sybase-needs-something-here'::character varying NOT NULL,
    name character varying(255) NOT NULL,
    value character varying(255),
    resource_id character varying(36) NOT NULL
);


ALTER TABLE public.resource_attribute OWNER TO csfeer;

--
-- Name: resource_policy; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_policy (
    resource_id character varying(36) NOT NULL,
    policy_id character varying(36) NOT NULL
);


ALTER TABLE public.resource_policy OWNER TO csfeer;

--
-- Name: resource_scope; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_scope (
    resource_id character varying(36) NOT NULL,
    scope_id character varying(36) NOT NULL
);


ALTER TABLE public.resource_scope OWNER TO csfeer;

--
-- Name: resource_server; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_server (
    id character varying(36) NOT NULL,
    allow_rs_remote_mgmt boolean DEFAULT false NOT NULL,
    policy_enforce_mode smallint NOT NULL,
    decision_strategy smallint DEFAULT 1 NOT NULL
);


ALTER TABLE public.resource_server OWNER TO csfeer;

--
-- Name: resource_server_perm_ticket; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_server_perm_ticket (
    id character varying(36) NOT NULL,
    owner character varying(255) NOT NULL,
    requester character varying(255) NOT NULL,
    created_timestamp bigint NOT NULL,
    granted_timestamp bigint,
    resource_id character varying(36) NOT NULL,
    scope_id character varying(36),
    resource_server_id character varying(36) NOT NULL,
    policy_id character varying(36)
);


ALTER TABLE public.resource_server_perm_ticket OWNER TO csfeer;

--
-- Name: resource_server_policy; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_server_policy (
    id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    description character varying(255),
    type character varying(255) NOT NULL,
    decision_strategy smallint,
    logic smallint,
    resource_server_id character varying(36) NOT NULL,
    owner character varying(255)
);


ALTER TABLE public.resource_server_policy OWNER TO csfeer;

--
-- Name: resource_server_resource; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_server_resource (
    id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    type character varying(255),
    icon_uri character varying(255),
    owner character varying(255) NOT NULL,
    resource_server_id character varying(36) NOT NULL,
    owner_managed_access boolean DEFAULT false NOT NULL,
    display_name character varying(255)
);


ALTER TABLE public.resource_server_resource OWNER TO csfeer;

--
-- Name: resource_server_scope; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_server_scope (
    id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    icon_uri character varying(255),
    resource_server_id character varying(36) NOT NULL,
    display_name character varying(255)
);


ALTER TABLE public.resource_server_scope OWNER TO csfeer;

--
-- Name: resource_uris; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.resource_uris (
    resource_id character varying(36) NOT NULL,
    value character varying(255) NOT NULL
);


ALTER TABLE public.resource_uris OWNER TO csfeer;

--
-- Name: revoked_token; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.revoked_token (
    id character varying(255) NOT NULL,
    expire bigint NOT NULL
);


ALTER TABLE public.revoked_token OWNER TO csfeer;

--
-- Name: role_attribute; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.role_attribute (
    id character varying(36) NOT NULL,
    role_id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    value character varying(255)
);


ALTER TABLE public.role_attribute OWNER TO csfeer;

--
-- Name: scope_mapping; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.scope_mapping (
    client_id character varying(36) NOT NULL,
    role_id character varying(36) NOT NULL
);


ALTER TABLE public.scope_mapping OWNER TO csfeer;

--
-- Name: scope_policy; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.scope_policy (
    scope_id character varying(36) NOT NULL,
    policy_id character varying(36) NOT NULL
);


ALTER TABLE public.scope_policy OWNER TO csfeer;

--
-- Name: server_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.server_config (
    server_config_key character varying(255) NOT NULL,
    value text NOT NULL,
    version integer DEFAULT 0
);


ALTER TABLE public.server_config OWNER TO csfeer;

--
-- Name: user_attribute; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_attribute (
    name character varying(255) NOT NULL,
    value character varying(255),
    user_id character varying(36) NOT NULL,
    id character varying(36) DEFAULT 'sybase-needs-something-here'::character varying NOT NULL,
    long_value_hash bytea,
    long_value_hash_lower_case bytea,
    long_value text
);


ALTER TABLE public.user_attribute OWNER TO csfeer;

--
-- Name: user_consent; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_consent (
    id character varying(36) NOT NULL,
    client_id character varying(255),
    user_id character varying(36) NOT NULL,
    created_date bigint,
    last_updated_date bigint,
    client_storage_provider character varying(36),
    external_client_id character varying(255)
);


ALTER TABLE public.user_consent OWNER TO csfeer;

--
-- Name: user_consent_client_scope; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_consent_client_scope (
    user_consent_id character varying(36) NOT NULL,
    scope_id character varying(36) NOT NULL
);


ALTER TABLE public.user_consent_client_scope OWNER TO csfeer;

--
-- Name: user_entity; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_entity (
    id character varying(36) NOT NULL,
    email character varying(255),
    email_constraint character varying(255),
    email_verified boolean DEFAULT false NOT NULL,
    enabled boolean DEFAULT false NOT NULL,
    federation_link character varying(255),
    first_name character varying(255),
    last_name character varying(255),
    realm_id character varying(255),
    username character varying(255),
    created_timestamp bigint,
    service_account_client_link character varying(255),
    not_before integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.user_entity OWNER TO csfeer;

--
-- Name: user_federation_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_federation_config (
    user_federation_provider_id character varying(36) NOT NULL,
    value character varying(255),
    name character varying(255) NOT NULL
);


ALTER TABLE public.user_federation_config OWNER TO csfeer;

--
-- Name: user_federation_mapper; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_federation_mapper (
    id character varying(36) NOT NULL,
    name character varying(255) NOT NULL,
    federation_provider_id character varying(36) NOT NULL,
    federation_mapper_type character varying(255) NOT NULL,
    realm_id character varying(36) NOT NULL
);


ALTER TABLE public.user_federation_mapper OWNER TO csfeer;

--
-- Name: user_federation_mapper_config; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_federation_mapper_config (
    user_federation_mapper_id character varying(36) NOT NULL,
    value character varying(255),
    name character varying(255) NOT NULL
);


ALTER TABLE public.user_federation_mapper_config OWNER TO csfeer;

--
-- Name: user_federation_provider; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_federation_provider (
    id character varying(36) NOT NULL,
    changed_sync_period integer,
    display_name character varying(255),
    full_sync_period integer,
    last_sync integer,
    priority integer,
    provider_name character varying(255),
    realm_id character varying(36)
);


ALTER TABLE public.user_federation_provider OWNER TO csfeer;

--
-- Name: user_group_membership; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_group_membership (
    group_id character varying(36) NOT NULL,
    user_id character varying(36) NOT NULL,
    membership_type character varying(255) NOT NULL
);


ALTER TABLE public.user_group_membership OWNER TO csfeer;

--
-- Name: user_required_action; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_required_action (
    user_id character varying(36) NOT NULL,
    required_action character varying(255) DEFAULT ' '::character varying NOT NULL
);


ALTER TABLE public.user_required_action OWNER TO csfeer;

--
-- Name: user_role_mapping; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.user_role_mapping (
    role_id character varying(255) NOT NULL,
    user_id character varying(36) NOT NULL
);


ALTER TABLE public.user_role_mapping OWNER TO csfeer;

--
-- Name: web_origins; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.web_origins (
    client_id character varying(36) NOT NULL,
    value character varying(255) NOT NULL
);


ALTER TABLE public.web_origins OWNER TO csfeer;

--
-- Name: workflow_state; Type: TABLE; Schema: public; Owner: csfeer
--

CREATE TABLE public.workflow_state (
    execution_id character varying(255) NOT NULL,
    resource_id character varying(255) NOT NULL,
    workflow_id character varying(255) NOT NULL,
    resource_type character varying(255),
    scheduled_step_id character varying(255),
    scheduled_step_timestamp bigint
);


ALTER TABLE public.workflow_state OWNER TO csfeer;

--
-- Data for Name: admin_event_entity; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.admin_event_entity (id, admin_event_time, realm_id, operation_type, auth_realm_id, auth_client_id, auth_user_id, ip_address, resource_path, representation, error, resource_type, details_json) FROM stdin;
\.


--
-- Data for Name: associated_policy; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.associated_policy (policy_id, associated_policy_id) FROM stdin;
\.


--
-- Data for Name: authentication_execution; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.authentication_execution (id, alias, authenticator, realm_id, flow_id, requirement, priority, authenticator_flow, auth_flow_id, auth_config) FROM stdin;
6f4c6e29-031f-4a2d-91a1-ff16b6994a3f	\N	auth-cookie	950f7f4b-1af6-4a64-bb5e-2561faa87127	61626dbf-8b26-4c8b-b9db-e12daabdeb09	2	10	f	\N	\N
e6c52bbd-4b5b-4aa5-8411-cdaba08f3d4f	\N	auth-spnego	950f7f4b-1af6-4a64-bb5e-2561faa87127	61626dbf-8b26-4c8b-b9db-e12daabdeb09	3	20	f	\N	\N
72682808-3c57-4738-bd14-ae6fa276330f	\N	identity-provider-redirector	950f7f4b-1af6-4a64-bb5e-2561faa87127	61626dbf-8b26-4c8b-b9db-e12daabdeb09	2	25	f	\N	\N
3659bc4e-5acd-477b-8d6f-7cf5fe85ec0b	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	61626dbf-8b26-4c8b-b9db-e12daabdeb09	2	30	t	6441cff6-18cf-4b02-8c67-905d64671c65	\N
9949d436-d069-4fdd-83ab-b61fb47c97dc	\N	auth-username-password-form	950f7f4b-1af6-4a64-bb5e-2561faa87127	6441cff6-18cf-4b02-8c67-905d64671c65	0	10	f	\N	\N
ab70dfb8-3ed2-4858-81cb-407fba30e262	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	6441cff6-18cf-4b02-8c67-905d64671c65	1	20	t	13af3e51-d435-49fb-a2c9-dc1121197306	\N
cb56fc64-29c7-4916-84c6-7b009f7c6e23	\N	conditional-user-configured	950f7f4b-1af6-4a64-bb5e-2561faa87127	13af3e51-d435-49fb-a2c9-dc1121197306	0	10	f	\N	\N
d94d6992-4e8f-4e2a-9e93-a4e68c178cd1	\N	conditional-credential	950f7f4b-1af6-4a64-bb5e-2561faa87127	13af3e51-d435-49fb-a2c9-dc1121197306	0	20	f	\N	facd8b06-3182-46ad-bad4-4559bfd3a793
5a8cb7dc-c5e4-4592-bce4-f8ed77bebea2	\N	auth-otp-form	950f7f4b-1af6-4a64-bb5e-2561faa87127	13af3e51-d435-49fb-a2c9-dc1121197306	2	30	f	\N	\N
d5e2c6ff-4c93-46d6-9cf1-e4ee59019e33	\N	webauthn-authenticator	950f7f4b-1af6-4a64-bb5e-2561faa87127	13af3e51-d435-49fb-a2c9-dc1121197306	3	40	f	\N	\N
fddc9497-c994-4b01-9887-325280ed8e64	\N	auth-recovery-authn-code-form	950f7f4b-1af6-4a64-bb5e-2561faa87127	13af3e51-d435-49fb-a2c9-dc1121197306	3	50	f	\N	\N
e59360aa-4a60-4191-ad48-05df1d0628eb	\N	direct-grant-validate-username	950f7f4b-1af6-4a64-bb5e-2561faa87127	522bdc6c-fb12-4b94-8d75-666ad8a60185	0	10	f	\N	\N
931230be-dfc7-4eb2-b069-535e7b320932	\N	direct-grant-validate-password	950f7f4b-1af6-4a64-bb5e-2561faa87127	522bdc6c-fb12-4b94-8d75-666ad8a60185	0	20	f	\N	\N
930e9845-0382-410b-b516-dcee8bd139ae	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	522bdc6c-fb12-4b94-8d75-666ad8a60185	1	30	t	33e6c478-f504-4537-b8cd-9251b9bfe1de	\N
36b3020b-9502-4f29-9430-4a88a03eea08	\N	conditional-user-configured	950f7f4b-1af6-4a64-bb5e-2561faa87127	33e6c478-f504-4537-b8cd-9251b9bfe1de	0	10	f	\N	\N
7ff78b10-c6a3-4412-8457-a7d24670bdd9	\N	direct-grant-validate-otp	950f7f4b-1af6-4a64-bb5e-2561faa87127	33e6c478-f504-4537-b8cd-9251b9bfe1de	0	20	f	\N	\N
87678eb0-40bc-4ce7-9059-d00f128ed4ff	\N	registration-page-form	950f7f4b-1af6-4a64-bb5e-2561faa87127	fbe0f1b4-4288-48a7-8d9e-4b83a347b8f0	0	10	t	e2a5fc47-c08e-4e2a-b835-221315073600	\N
8d49942e-a2bd-4086-9f17-d970765c88b5	\N	registration-user-creation	950f7f4b-1af6-4a64-bb5e-2561faa87127	e2a5fc47-c08e-4e2a-b835-221315073600	0	20	f	\N	\N
2dad5d64-9b19-4770-9d3f-1a90ede3c645	\N	registration-password-action	950f7f4b-1af6-4a64-bb5e-2561faa87127	e2a5fc47-c08e-4e2a-b835-221315073600	0	50	f	\N	\N
476ef423-4501-45f7-940c-6acb67fda6a9	\N	registration-recaptcha-action	950f7f4b-1af6-4a64-bb5e-2561faa87127	e2a5fc47-c08e-4e2a-b835-221315073600	3	60	f	\N	\N
d8ce5f28-e405-4916-a709-66819e14cabd	\N	registration-terms-and-conditions	950f7f4b-1af6-4a64-bb5e-2561faa87127	e2a5fc47-c08e-4e2a-b835-221315073600	3	70	f	\N	\N
ed7b6e6e-0ca9-4dde-836e-89fb8fcae0c6	\N	reset-credentials-choose-user	950f7f4b-1af6-4a64-bb5e-2561faa87127	275b1fe4-338d-4c87-9707-5c6008b60fcc	0	10	f	\N	\N
7bd685f2-3cf7-42d2-aacd-7b5957d0e6cb	\N	reset-credential-email	950f7f4b-1af6-4a64-bb5e-2561faa87127	275b1fe4-338d-4c87-9707-5c6008b60fcc	0	20	f	\N	\N
3f0ac6e9-7b49-4111-b3ea-e5f2055a653e	\N	reset-password	950f7f4b-1af6-4a64-bb5e-2561faa87127	275b1fe4-338d-4c87-9707-5c6008b60fcc	0	30	f	\N	\N
22076eb6-4606-47eb-bc9f-3a0359ca5aab	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	275b1fe4-338d-4c87-9707-5c6008b60fcc	1	40	t	ea39d0de-50e7-4445-8153-b50a21c79417	\N
07bc691d-32b9-4488-b87a-dc01f0914608	\N	conditional-user-configured	950f7f4b-1af6-4a64-bb5e-2561faa87127	ea39d0de-50e7-4445-8153-b50a21c79417	0	10	f	\N	\N
48aaec5d-f5a8-4dae-bcba-abf5d37dd7cf	\N	reset-otp	950f7f4b-1af6-4a64-bb5e-2561faa87127	ea39d0de-50e7-4445-8153-b50a21c79417	0	20	f	\N	\N
5eacb812-cf9f-4b7e-b13f-e2ad8ab1e83e	\N	client-secret	950f7f4b-1af6-4a64-bb5e-2561faa87127	6c6e1bff-c862-4bde-b219-7877e79fdbb2	2	10	f	\N	\N
d3463d50-dbb6-4861-ab87-fe6122064dee	\N	client-jwt	950f7f4b-1af6-4a64-bb5e-2561faa87127	6c6e1bff-c862-4bde-b219-7877e79fdbb2	2	20	f	\N	\N
1df82b54-76d8-4e59-85ef-af059835940e	\N	client-secret-jwt	950f7f4b-1af6-4a64-bb5e-2561faa87127	6c6e1bff-c862-4bde-b219-7877e79fdbb2	2	30	f	\N	\N
9a3dfdeb-ce54-4e55-b92f-95121ac80be1	\N	client-x509	950f7f4b-1af6-4a64-bb5e-2561faa87127	6c6e1bff-c862-4bde-b219-7877e79fdbb2	2	40	f	\N	\N
4d25287d-2cd3-403d-b37c-402419d803d5	\N	idp-review-profile	950f7f4b-1af6-4a64-bb5e-2561faa87127	a0df8b1b-ad8f-4648-a70a-90679d1ada73	0	10	f	\N	d9fe044f-89a7-42fa-988e-151b033f8955
50508f16-8935-4834-a119-576c6b85b73b	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	a0df8b1b-ad8f-4648-a70a-90679d1ada73	0	20	t	ae42222d-2f83-43e1-8e0f-1f67e86b6c13	\N
f2cf5b94-93e6-4ec5-9a9e-175dd952ffda	\N	idp-create-user-if-unique	950f7f4b-1af6-4a64-bb5e-2561faa87127	ae42222d-2f83-43e1-8e0f-1f67e86b6c13	2	10	f	\N	e188aa65-51e1-4aaf-aa4c-02ba8628c463
c13004b9-0c83-4c45-aa50-41d81af46bfd	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	ae42222d-2f83-43e1-8e0f-1f67e86b6c13	2	20	t	0793433b-0a4c-48bc-90f9-4640ea0444ca	\N
683707fa-a352-49e0-923b-36f8a1d4d6f3	\N	idp-confirm-link	950f7f4b-1af6-4a64-bb5e-2561faa87127	0793433b-0a4c-48bc-90f9-4640ea0444ca	0	10	f	\N	\N
3d598398-5091-4d80-a2c9-3b8487c7dd30	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	0793433b-0a4c-48bc-90f9-4640ea0444ca	0	20	t	aa55f70a-07c6-4282-ba85-c72b3278f0cf	\N
d9f52435-12a0-494f-a7f4-0e1a81622889	\N	idp-email-verification	950f7f4b-1af6-4a64-bb5e-2561faa87127	aa55f70a-07c6-4282-ba85-c72b3278f0cf	2	10	f	\N	\N
8caa81fb-89e7-4d66-9fcc-3db1fda2df25	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	aa55f70a-07c6-4282-ba85-c72b3278f0cf	2	20	t	8f0f5061-792f-4c63-9fa0-0e90d0402cff	\N
26ac35e3-c9b7-4fb0-9fd9-3865400bae42	\N	idp-username-password-form	950f7f4b-1af6-4a64-bb5e-2561faa87127	8f0f5061-792f-4c63-9fa0-0e90d0402cff	0	10	f	\N	\N
795fd2c2-b893-4e6f-bb5b-c974e1c8138c	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	8f0f5061-792f-4c63-9fa0-0e90d0402cff	1	20	t	e5acdc7b-41a3-4174-b6fd-1439cb243b9a	\N
750eec48-5a9c-4ba7-a498-983a4231cdd4	\N	conditional-user-configured	950f7f4b-1af6-4a64-bb5e-2561faa87127	e5acdc7b-41a3-4174-b6fd-1439cb243b9a	0	10	f	\N	\N
9b72e996-397e-4869-97fc-936bf8367bc7	\N	conditional-credential	950f7f4b-1af6-4a64-bb5e-2561faa87127	e5acdc7b-41a3-4174-b6fd-1439cb243b9a	0	20	f	\N	cfca1a88-c1d4-4a45-a504-e2f14e882fd7
212d7f31-03a6-482a-8c2e-26add5732abb	\N	auth-otp-form	950f7f4b-1af6-4a64-bb5e-2561faa87127	e5acdc7b-41a3-4174-b6fd-1439cb243b9a	2	30	f	\N	\N
695031c8-7f38-4965-946d-88839038afef	\N	webauthn-authenticator	950f7f4b-1af6-4a64-bb5e-2561faa87127	e5acdc7b-41a3-4174-b6fd-1439cb243b9a	3	40	f	\N	\N
bd57dca2-3f61-4776-a325-641878c930bf	\N	auth-recovery-authn-code-form	950f7f4b-1af6-4a64-bb5e-2561faa87127	e5acdc7b-41a3-4174-b6fd-1439cb243b9a	3	50	f	\N	\N
026316be-7ded-458a-a94e-efc97c384363	\N	http-basic-authenticator	950f7f4b-1af6-4a64-bb5e-2561faa87127	48532089-306c-47c1-85ae-6bbb5cc9ff1e	0	10	f	\N	\N
0cd0b183-713d-4cb4-b01b-e0e4b583e39e	\N	docker-http-basic-authenticator	950f7f4b-1af6-4a64-bb5e-2561faa87127	fdeb50ca-1ec0-4808-96c8-6587bdfdb939	0	10	f	\N	\N
4b392361-9572-4c15-8745-7fd111126961	\N	idp-email-verification	c55a12d3-a06b-43f4-b990-28390a55a7af	96b90cbe-406e-4689-9be2-aecdc81688d9	2	10	f	\N	\N
f9289b38-84e2-4412-9ad3-959cbf4794ad	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	96b90cbe-406e-4689-9be2-aecdc81688d9	2	20	t	63a73b68-332c-4e25-8e86-d47cbdfaedf7	\N
6f500688-3696-4a16-b5f8-8b715a411f2a	\N	conditional-user-configured	c55a12d3-a06b-43f4-b990-28390a55a7af	d959675f-595a-41b6-b094-7e6e97caf3e1	0	10	f	\N	\N
df31b091-dd5e-447e-b75b-0f53d96b6582	\N	auth-otp-form	c55a12d3-a06b-43f4-b990-28390a55a7af	d959675f-595a-41b6-b094-7e6e97caf3e1	2	20	f	\N	\N
20affeeb-9346-4786-8d4e-632f33da185d	\N	webauthn-authenticator	c55a12d3-a06b-43f4-b990-28390a55a7af	d959675f-595a-41b6-b094-7e6e97caf3e1	3	30	f	\N	\N
98a7b4bc-160c-4e73-9ee5-e5668bf6d3ee	\N	auth-recovery-authn-code-form	c55a12d3-a06b-43f4-b990-28390a55a7af	d959675f-595a-41b6-b094-7e6e97caf3e1	3	40	f	\N	\N
9712033f-afd5-4d92-8b46-8959d54eb222	\N	conditional-user-configured	c55a12d3-a06b-43f4-b990-28390a55a7af	d96d874b-2bd5-4dd6-a1c5-61fb3742410e	0	10	f	\N	\N
8213b300-b785-41d1-9ea1-471580dc7600	\N	organization	c55a12d3-a06b-43f4-b990-28390a55a7af	d96d874b-2bd5-4dd6-a1c5-61fb3742410e	2	20	f	\N	\N
d2c846c3-ac44-4897-91e9-87a0c1b882c0	\N	conditional-user-configured	c55a12d3-a06b-43f4-b990-28390a55a7af	e6198892-644c-43da-95bf-ba8695364d39	0	10	f	\N	\N
f5a65d03-9015-490c-bd2f-db71482eacba	\N	direct-grant-validate-otp	c55a12d3-a06b-43f4-b990-28390a55a7af	e6198892-644c-43da-95bf-ba8695364d39	0	20	f	\N	\N
37d2686f-9774-4b40-bf0a-c54c0447b675	\N	conditional-user-configured	c55a12d3-a06b-43f4-b990-28390a55a7af	88c243ff-8ace-4a52-8744-58a8ee59001a	0	10	f	\N	\N
e2717c59-1f3a-4119-acf5-bbe66e72f46d	\N	idp-add-organization-member	c55a12d3-a06b-43f4-b990-28390a55a7af	88c243ff-8ace-4a52-8744-58a8ee59001a	0	20	f	\N	\N
21130d89-e0f0-4ac3-aa69-7e6c44e50882	\N	conditional-user-configured	c55a12d3-a06b-43f4-b990-28390a55a7af	fdfc3258-fc67-4534-b5f8-f52f65257633	0	10	f	\N	\N
8703e85f-81d3-4d4b-9fc6-0727b65f7043	\N	auth-otp-form	c55a12d3-a06b-43f4-b990-28390a55a7af	fdfc3258-fc67-4534-b5f8-f52f65257633	2	20	f	\N	\N
6fa64679-830d-484f-ba77-abc9f3680858	\N	webauthn-authenticator	c55a12d3-a06b-43f4-b990-28390a55a7af	fdfc3258-fc67-4534-b5f8-f52f65257633	3	30	f	\N	\N
4aaacaeb-477e-4bd7-ac1d-21b37c7e012c	\N	auth-recovery-authn-code-form	c55a12d3-a06b-43f4-b990-28390a55a7af	fdfc3258-fc67-4534-b5f8-f52f65257633	3	40	f	\N	\N
df29ad90-120b-45ea-bc77-cf5df2482fcf	\N	idp-confirm-link	c55a12d3-a06b-43f4-b990-28390a55a7af	d9a6ac29-8792-4e0f-866e-baf2df32a191	0	10	f	\N	\N
12f6cd9b-0f16-47f5-9b58-1e90b2ee7594	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	d9a6ac29-8792-4e0f-866e-baf2df32a191	0	20	t	96b90cbe-406e-4689-9be2-aecdc81688d9	\N
be18131f-d7f9-46e5-ac86-4c62335be4eb	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	98cb3e1d-ccd4-4851-a486-10fdb20a2e47	1	10	t	d96d874b-2bd5-4dd6-a1c5-61fb3742410e	\N
c943ecf5-dbb9-4d30-ac3d-f3e0d75c7018	\N	conditional-user-configured	c55a12d3-a06b-43f4-b990-28390a55a7af	286cd6ca-97fb-45b2-ab27-66fd03f83b15	0	10	f	\N	\N
5396c609-c56d-46ab-b521-b69a9882b252	\N	reset-otp	c55a12d3-a06b-43f4-b990-28390a55a7af	286cd6ca-97fb-45b2-ab27-66fd03f83b15	0	20	f	\N	\N
782e8c8a-4a50-4b45-86ec-1e5cd7153aff	\N	idp-create-user-if-unique	c55a12d3-a06b-43f4-b990-28390a55a7af	da01a5f0-e3fa-4cd0-b9d6-35d5d83a7003	2	10	f	\N	689e5ee2-447d-464a-9986-1e9514a14120
c2081db2-ef74-476a-a4cb-840fc8ccb918	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	da01a5f0-e3fa-4cd0-b9d6-35d5d83a7003	2	20	t	d9a6ac29-8792-4e0f-866e-baf2df32a191	\N
c8f2f9ec-ed47-44b5-bf0a-5ce9e7e6402a	\N	idp-username-password-form	c55a12d3-a06b-43f4-b990-28390a55a7af	63a73b68-332c-4e25-8e86-d47cbdfaedf7	0	10	f	\N	\N
8d9b3e37-17f9-4617-903f-00ff97a9718a	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	63a73b68-332c-4e25-8e86-d47cbdfaedf7	1	20	t	fdfc3258-fc67-4534-b5f8-f52f65257633	\N
b71f3c29-7ca3-40ab-a382-7784d48fe59d	\N	auth-cookie	c55a12d3-a06b-43f4-b990-28390a55a7af	f9d5cc86-3825-47cf-ae7f-c07abe687f11	2	10	f	\N	\N
443ccfe2-d7d4-408b-9581-654f7d7cedc2	\N	auth-spnego	c55a12d3-a06b-43f4-b990-28390a55a7af	f9d5cc86-3825-47cf-ae7f-c07abe687f11	3	20	f	\N	\N
9472c2a5-8ae8-4658-826c-1b949def3884	\N	identity-provider-redirector	c55a12d3-a06b-43f4-b990-28390a55a7af	f9d5cc86-3825-47cf-ae7f-c07abe687f11	2	25	f	\N	\N
7cd1c9fd-fc6f-43bf-92c8-0f137358c55e	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	f9d5cc86-3825-47cf-ae7f-c07abe687f11	2	26	t	98cb3e1d-ccd4-4851-a486-10fdb20a2e47	\N
bfa73a60-35d3-4ced-9b1c-d81a7aed43f1	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	f9d5cc86-3825-47cf-ae7f-c07abe687f11	2	30	t	5533725b-1572-4d61-9fe1-6fcf641911b9	\N
07b1d0e7-4662-4dab-b67a-3c7391f29eba	\N	client-secret	c55a12d3-a06b-43f4-b990-28390a55a7af	5ceaf82b-70da-4968-b87b-129337abe077	2	10	f	\N	\N
932d19ad-7e75-4456-974f-db7cc0ae52b1	\N	client-jwt	c55a12d3-a06b-43f4-b990-28390a55a7af	5ceaf82b-70da-4968-b87b-129337abe077	2	20	f	\N	\N
97fe6e79-a18a-42e8-8767-18c98aba17ec	\N	client-secret-jwt	c55a12d3-a06b-43f4-b990-28390a55a7af	5ceaf82b-70da-4968-b87b-129337abe077	2	30	f	\N	\N
15b5512b-f0aa-4139-a23c-64ca26f4867d	\N	client-x509	c55a12d3-a06b-43f4-b990-28390a55a7af	5ceaf82b-70da-4968-b87b-129337abe077	2	40	f	\N	\N
a382827f-3077-44d9-a981-209d5d00ab86	\N	direct-grant-validate-username	c55a12d3-a06b-43f4-b990-28390a55a7af	2f47735e-097d-420e-8486-33b13e85bddb	0	10	f	\N	\N
9994eea8-f957-4e00-984f-8f3ea70837d2	\N	direct-grant-validate-password	c55a12d3-a06b-43f4-b990-28390a55a7af	2f47735e-097d-420e-8486-33b13e85bddb	0	20	f	\N	\N
8a861e77-ae8b-48a8-954c-ce6796cc9a27	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	2f47735e-097d-420e-8486-33b13e85bddb	1	30	t	e6198892-644c-43da-95bf-ba8695364d39	\N
9ddfa60e-6cf6-4f2e-aff8-c88346bd759e	\N	docker-http-basic-authenticator	c55a12d3-a06b-43f4-b990-28390a55a7af	2c5bf88c-6a6b-449b-9f84-b62d149a9291	0	10	f	\N	\N
4df3d07d-cef9-4540-ba11-fa9426a83bed	\N	idp-review-profile	c55a12d3-a06b-43f4-b990-28390a55a7af	385da139-ce9e-469b-81a9-37e9e765c315	0	10	f	\N	6adc273b-58e9-424f-bd48-4fe271fe4d23
95bb14a4-5b99-4196-afe7-51b834fedbdc	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	385da139-ce9e-469b-81a9-37e9e765c315	0	20	t	da01a5f0-e3fa-4cd0-b9d6-35d5d83a7003	\N
e1ed52e0-25bc-4c58-b9b4-ccb142378414	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	385da139-ce9e-469b-81a9-37e9e765c315	1	50	t	88c243ff-8ace-4a52-8744-58a8ee59001a	\N
3d5f50bf-f385-4f7c-b44f-c3a7b3c388e1	\N	auth-username-password-form	c55a12d3-a06b-43f4-b990-28390a55a7af	5533725b-1572-4d61-9fe1-6fcf641911b9	0	10	f	\N	\N
bd89f15c-fc26-4883-b905-8883770043c4	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	5533725b-1572-4d61-9fe1-6fcf641911b9	1	20	t	d959675f-595a-41b6-b094-7e6e97caf3e1	\N
e440d251-9d1b-4461-a23b-5af10a005322	\N	registration-page-form	c55a12d3-a06b-43f4-b990-28390a55a7af	90668b03-0d53-453d-98c7-312f13d16cf5	0	10	t	8a394da5-1973-4940-a7c7-f0e00616bdb0	\N
76da02b8-20c5-4215-b7f2-c00514381f6c	\N	registration-user-creation	c55a12d3-a06b-43f4-b990-28390a55a7af	8a394da5-1973-4940-a7c7-f0e00616bdb0	0	20	f	\N	\N
eb4cad38-e7b2-4d25-a52b-b0220980145b	\N	registration-password-action	c55a12d3-a06b-43f4-b990-28390a55a7af	8a394da5-1973-4940-a7c7-f0e00616bdb0	0	50	f	\N	\N
1085db9e-e170-4fcd-92da-eea4621802ae	\N	registration-recaptcha-action	c55a12d3-a06b-43f4-b990-28390a55a7af	8a394da5-1973-4940-a7c7-f0e00616bdb0	3	60	f	\N	\N
93241a01-d0f6-4666-822c-fa269f17503d	\N	registration-terms-and-conditions	c55a12d3-a06b-43f4-b990-28390a55a7af	8a394da5-1973-4940-a7c7-f0e00616bdb0	3	70	f	\N	\N
369b3416-3332-45dc-ad5b-2eed32c77fca	\N	reset-credentials-choose-user	c55a12d3-a06b-43f4-b990-28390a55a7af	dfcd5483-03a4-4ca1-97ed-275d9e35434c	0	10	f	\N	\N
59e653f3-e3a4-4b01-a009-66703a9adb55	\N	reset-credential-email	c55a12d3-a06b-43f4-b990-28390a55a7af	dfcd5483-03a4-4ca1-97ed-275d9e35434c	0	20	f	\N	\N
8bfdabea-d243-41e2-8795-4aa3ae4970b6	\N	reset-password	c55a12d3-a06b-43f4-b990-28390a55a7af	dfcd5483-03a4-4ca1-97ed-275d9e35434c	0	30	f	\N	\N
91c646b6-3db2-4900-957a-f86a8db5a345	\N	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	dfcd5483-03a4-4ca1-97ed-275d9e35434c	1	40	t	286cd6ca-97fb-45b2-ab27-66fd03f83b15	\N
46be753e-b981-47e1-8b45-c4f15b85215c	\N	http-basic-authenticator	c55a12d3-a06b-43f4-b990-28390a55a7af	014097e1-97f9-4320-a19d-7a899595c9ff	0	10	f	\N	\N
\.


--
-- Data for Name: authentication_flow; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.authentication_flow (id, alias, description, realm_id, provider_id, top_level, built_in) FROM stdin;
61626dbf-8b26-4c8b-b9db-e12daabdeb09	browser	Browser based authentication	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	t	t
6441cff6-18cf-4b02-8c67-905d64671c65	forms	Username, password, otp and other auth forms.	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
13af3e51-d435-49fb-a2c9-dc1121197306	Browser - Conditional 2FA	Flow to determine if any 2FA is required for the authentication	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
522bdc6c-fb12-4b94-8d75-666ad8a60185	direct grant	OpenID Connect Resource Owner Grant	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	t	t
33e6c478-f504-4537-b8cd-9251b9bfe1de	Direct Grant - Conditional OTP	Flow to determine if the OTP is required for the authentication	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
fbe0f1b4-4288-48a7-8d9e-4b83a347b8f0	registration	Registration flow	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	t	t
e2a5fc47-c08e-4e2a-b835-221315073600	registration form	Registration form	950f7f4b-1af6-4a64-bb5e-2561faa87127	form-flow	f	t
275b1fe4-338d-4c87-9707-5c6008b60fcc	reset credentials	Reset credentials for a user if they forgot their password or something	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	t	t
ea39d0de-50e7-4445-8153-b50a21c79417	Reset - Conditional OTP	Flow to determine if the OTP should be reset or not. Set to REQUIRED to force.	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
6c6e1bff-c862-4bde-b219-7877e79fdbb2	clients	Base authentication for clients	950f7f4b-1af6-4a64-bb5e-2561faa87127	client-flow	t	t
a0df8b1b-ad8f-4648-a70a-90679d1ada73	first broker login	Actions taken after first broker login with identity provider account, which is not yet linked to any Keycloak account	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	t	t
ae42222d-2f83-43e1-8e0f-1f67e86b6c13	User creation or linking	Flow for the existing/non-existing user alternatives	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
0793433b-0a4c-48bc-90f9-4640ea0444ca	Handle Existing Account	Handle what to do if there is existing account with same email/username like authenticated identity provider	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
aa55f70a-07c6-4282-ba85-c72b3278f0cf	Account verification options	Method with which to verify the existing account	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
8f0f5061-792f-4c63-9fa0-0e90d0402cff	Verify Existing Account by Re-authentication	Reauthentication of existing account	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
e5acdc7b-41a3-4174-b6fd-1439cb243b9a	First broker login - Conditional 2FA	Flow to determine if any 2FA is required for the authentication	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	f	t
48532089-306c-47c1-85ae-6bbb5cc9ff1e	saml ecp	SAML ECP Profile Authentication Flow	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	t	t
fdeb50ca-1ec0-4808-96c8-6587bdfdb939	docker auth	Used by Docker clients to authenticate against the IDP	950f7f4b-1af6-4a64-bb5e-2561faa87127	basic-flow	t	t
96b90cbe-406e-4689-9be2-aecdc81688d9	Account verification options	Method with which to verity the existing account	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
d959675f-595a-41b6-b094-7e6e97caf3e1	Browser - Conditional 2FA	Flow to determine if any 2FA is required for the authentication	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
d96d874b-2bd5-4dd6-a1c5-61fb3742410e	Browser - Conditional Organization	Flow to determine if the organization identity-first login is to be used	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
e6198892-644c-43da-95bf-ba8695364d39	Direct Grant - Conditional OTP	Flow to determine if the OTP is required for the authentication	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
88c243ff-8ace-4a52-8744-58a8ee59001a	First Broker Login - Conditional Organization	Flow to determine if the authenticator that adds organization members is to be used	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
fdfc3258-fc67-4534-b5f8-f52f65257633	First broker login - Conditional 2FA	Flow to determine if any 2FA is required for the authentication	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
d9a6ac29-8792-4e0f-866e-baf2df32a191	Handle Existing Account	Handle what to do if there is existing account with same email/username like authenticated identity provider	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
98cb3e1d-ccd4-4851-a486-10fdb20a2e47	Organization	\N	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
286cd6ca-97fb-45b2-ab27-66fd03f83b15	Reset - Conditional OTP	Flow to determine if the OTP should be reset or not. Set to REQUIRED to force.	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
da01a5f0-e3fa-4cd0-b9d6-35d5d83a7003	User creation or linking	Flow for the existing/non-existing user alternatives	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
63a73b68-332c-4e25-8e86-d47cbdfaedf7	Verify Existing Account by Re-authentication	Reauthentication of existing account	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
f9d5cc86-3825-47cf-ae7f-c07abe687f11	browser	Browser based authentication	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	t	t
5ceaf82b-70da-4968-b87b-129337abe077	clients	Base authentication for clients	c55a12d3-a06b-43f4-b990-28390a55a7af	client-flow	t	t
2f47735e-097d-420e-8486-33b13e85bddb	direct grant	OpenID Connect Resource Owner Grant	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	t	t
2c5bf88c-6a6b-449b-9f84-b62d149a9291	docker auth	Used by Docker clients to authenticate against the IDP	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	t	t
385da139-ce9e-469b-81a9-37e9e765c315	first broker login	Actions taken after first broker login with identity provider account, which is not yet linked to any Keycloak account	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	t	t
5533725b-1572-4d61-9fe1-6fcf641911b9	forms	Username, password, otp and other auth forms.	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	f	t
90668b03-0d53-453d-98c7-312f13d16cf5	registration	Registration flow	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	t	t
8a394da5-1973-4940-a7c7-f0e00616bdb0	registration form	Registration form	c55a12d3-a06b-43f4-b990-28390a55a7af	form-flow	f	t
dfcd5483-03a4-4ca1-97ed-275d9e35434c	reset credentials	Reset credentials for a user if they forgot their password or something	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	t	t
014097e1-97f9-4320-a19d-7a899595c9ff	saml ecp	SAML ECP Profile Authentication Flow	c55a12d3-a06b-43f4-b990-28390a55a7af	basic-flow	t	t
\.


--
-- Data for Name: authenticator_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.authenticator_config (id, alias, realm_id) FROM stdin;
facd8b06-3182-46ad-bad4-4559bfd3a793	browser-conditional-credential	950f7f4b-1af6-4a64-bb5e-2561faa87127
d9fe044f-89a7-42fa-988e-151b033f8955	review profile config	950f7f4b-1af6-4a64-bb5e-2561faa87127
e188aa65-51e1-4aaf-aa4c-02ba8628c463	create unique user config	950f7f4b-1af6-4a64-bb5e-2561faa87127
cfca1a88-c1d4-4a45-a504-e2f14e882fd7	first-broker-login-conditional-credential	950f7f4b-1af6-4a64-bb5e-2561faa87127
689e5ee2-447d-464a-9986-1e9514a14120	create unique user config	c55a12d3-a06b-43f4-b990-28390a55a7af
6adc273b-58e9-424f-bd48-4fe271fe4d23	review profile config	c55a12d3-a06b-43f4-b990-28390a55a7af
\.


--
-- Data for Name: authenticator_config_entry; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.authenticator_config_entry (authenticator_id, value, name) FROM stdin;
cfca1a88-c1d4-4a45-a504-e2f14e882fd7	webauthn-passwordless	credentials
d9fe044f-89a7-42fa-988e-151b033f8955	missing	update.profile.on.first.login
e188aa65-51e1-4aaf-aa4c-02ba8628c463	false	require.password.update.after.registration
facd8b06-3182-46ad-bad4-4559bfd3a793	webauthn-passwordless	credentials
689e5ee2-447d-464a-9986-1e9514a14120	false	require.password.update.after.registration
6adc273b-58e9-424f-bd48-4fe271fe4d23	missing	update.profile.on.first.login
\.


--
-- Data for Name: broker_link; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.broker_link (identity_provider, storage_provider_id, realm_id, broker_user_id, broker_username, token, user_id) FROM stdin;
\.


--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client (id, enabled, full_scope_allowed, client_id, not_before, public_client, secret, base_url, bearer_only, management_url, surrogate_auth_required, realm_id, protocol, node_rereg_timeout, frontchannel_logout, consent_required, name, service_accounts_enabled, client_authenticator_type, root_url, description, registration_token, standard_flow_enabled, implicit_flow_enabled, direct_access_grants_enabled, always_display_in_console) FROM stdin;
a8ce899c-8a3d-4391-98dc-72610c85b515	t	f	master-realm	0	f	\N	\N	t	\N	f	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N	0	f	f	master Realm	f	client-secret	\N	\N	\N	t	f	f	f
70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	f	account	0	t	\N	/realms/master/account/	f	\N	f	950f7f4b-1af6-4a64-bb5e-2561faa87127	openid-connect	0	f	f	${client_account}	f	client-secret	${authBaseUrl}	\N	\N	t	f	f	f
640d1fae-9a47-46dc-81d3-8ed39870984a	t	f	account-console	0	t	\N	/realms/master/account/	f	\N	f	950f7f4b-1af6-4a64-bb5e-2561faa87127	openid-connect	0	f	f	${client_account-console}	f	client-secret	${authBaseUrl}	\N	\N	t	f	f	f
4af7bbb0-5dbf-4fdd-b730-79b146a12050	t	f	broker	0	f	\N	\N	t	\N	f	950f7f4b-1af6-4a64-bb5e-2561faa87127	openid-connect	0	f	f	${client_broker}	f	client-secret	\N	\N	\N	t	f	f	f
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	t	t	security-admin-console	0	t	\N	/admin/master/console/	f	\N	f	950f7f4b-1af6-4a64-bb5e-2561faa87127	openid-connect	0	f	f	${client_security-admin-console}	f	client-secret	${authAdminUrl}	\N	\N	t	f	f	f
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	t	t	admin-cli	0	t	\N	\N	f	\N	f	950f7f4b-1af6-4a64-bb5e-2561faa87127	openid-connect	0	f	f	${client_admin-cli}	f	client-secret	\N	\N	\N	f	f	t	f
ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	f	csfeer-realm	0	f	\N	\N	t	\N	f	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N	0	f	f	csfeer Realm	f	client-secret	\N	\N	\N	t	f	f	f
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	f	account	0	t	\N	/realms/csfeer/account/	f	\N	f	c55a12d3-a06b-43f4-b990-28390a55a7af	openid-connect	0	f	f	${client_account}	f	client-secret	${authBaseUrl}	\N	\N	t	f	f	f
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	t	f	account-console	0	t	\N	/realms/csfeer/account/	f	\N	f	c55a12d3-a06b-43f4-b990-28390a55a7af	openid-connect	0	f	f	${client_account-console}	f	client-secret	${authBaseUrl}	\N	\N	t	f	f	f
3f723df7-fc18-4a13-9a0b-3df75da808d7	t	t	admin-cli	0	t	\N	\N	f	\N	f	c55a12d3-a06b-43f4-b990-28390a55a7af	openid-connect	0	f	f	${client_admin-cli}	f	client-secret	\N	\N	\N	f	f	t	f
b141edca-aa19-47f5-87be-23de76c8a44f	t	f	broker	0	f	\N	\N	t	\N	f	c55a12d3-a06b-43f4-b990-28390a55a7af	openid-connect	0	f	f	${client_broker}	f	client-secret	\N	\N	\N	t	f	f	f
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	f	realm-management	0	f	\N	\N	t	\N	f	c55a12d3-a06b-43f4-b990-28390a55a7af	openid-connect	0	f	f	${client_realm-management}	f	client-secret	\N	\N	\N	t	f	f	f
043917f3-a51e-4661-83c1-41b19f4ee3fe	t	t	security-admin-console	0	t	\N	/admin/csfeer/console/	f	\N	f	c55a12d3-a06b-43f4-b990-28390a55a7af	openid-connect	0	f	f	${client_security-admin-console}	f	client-secret	${authAdminUrl}	\N	\N	t	f	f	f
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	t	t	csfeer-auth	0	f	shhhhhhhh	\N	f	\N	f	950f7f4b-1af6-4a64-bb5e-2561faa87127	openid-connect	-1	f	f	\N	t	client-secret	\N	\N	\N	f	f	f	f
83ab17ea-566c-43b4-abc5-847346d7485a	t	t	csfeer-auth	0	f	shhhhhhhh	http://ui.csfeer:8000	f	http://ui.csfeer:8000	f	c55a12d3-a06b-43f4-b990-28390a55a7af	openid-connect	-1	t	f		f	client-secret	http://ui.csfeer:8000		\N	t	f	f	t
\.


--
-- Data for Name: client_attributes; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client_attributes (client_id, name, value) FROM stdin;
70f8e924-f945-4a2a-b7f2-130505a5f8f7	post.logout.redirect.uris	+
640d1fae-9a47-46dc-81d3-8ed39870984a	post.logout.redirect.uris	+
640d1fae-9a47-46dc-81d3-8ed39870984a	pkce.code.challenge.method	S256
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	post.logout.redirect.uris	+
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	pkce.code.challenge.method	S256
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	client.use.lightweight.access.token.enabled	true
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	client.use.lightweight.access.token.enabled	true
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	realm_client	false
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	post.logout.redirect.uris	+
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	realm_client	false
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	post.logout.redirect.uris	+
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	pkce.code.challenge.method	S256
3f723df7-fc18-4a13-9a0b-3df75da808d7	realm_client	false
3f723df7-fc18-4a13-9a0b-3df75da808d7	client.use.lightweight.access.token.enabled	true
3f723df7-fc18-4a13-9a0b-3df75da808d7	post.logout.redirect.uris	+
b141edca-aa19-47f5-87be-23de76c8a44f	realm_client	true
b141edca-aa19-47f5-87be-23de76c8a44f	post.logout.redirect.uris	+
83ab17ea-566c-43b4-abc5-847346d7485a	realm_client	false
83ab17ea-566c-43b4-abc5-847346d7485a	oidc.ciba.grant.enabled	false
83ab17ea-566c-43b4-abc5-847346d7485a	client.secret.creation.time	1759849649
83ab17ea-566c-43b4-abc5-847346d7485a	backchannel.logout.session.required	true
83ab17ea-566c-43b4-abc5-847346d7485a	standard.token.exchange.enabled	false
83ab17ea-566c-43b4-abc5-847346d7485a	frontchannel.logout.session.required	true
83ab17ea-566c-43b4-abc5-847346d7485a	post.logout.redirect.uris	http://localhost:8000/oidc/logout_by_op##http://127.0.0.1:8000/oidc/logout_by_o##http://ui.csfeer:8000/oidc/logout_by_o
83ab17ea-566c-43b4-abc5-847346d7485a	display.on.consent.screen	false
83ab17ea-566c-43b4-abc5-847346d7485a	oauth2.device.authorization.grant.enabled	false
83ab17ea-566c-43b4-abc5-847346d7485a	use.jwks.url	false
83ab17ea-566c-43b4-abc5-847346d7485a	backchannel.logout.revoke.offline.tokens	false
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	realm_client	true
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	post.logout.redirect.uris	+
043917f3-a51e-4661-83c1-41b19f4ee3fe	realm_client	false
043917f3-a51e-4661-83c1-41b19f4ee3fe	client.use.lightweight.access.token.enabled	true
043917f3-a51e-4661-83c1-41b19f4ee3fe	post.logout.redirect.uris	+
043917f3-a51e-4661-83c1-41b19f4ee3fe	pkce.code.challenge.method	S256
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	client.use.lightweight.access.token.enabled	true
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	is_temporary_admin	true
\.


--
-- Data for Name: client_auth_flow_bindings; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client_auth_flow_bindings (client_id, flow_id, binding_name) FROM stdin;
\.


--
-- Data for Name: client_initial_access; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client_initial_access (id, realm_id, "timestamp", expiration, count, remaining_count) FROM stdin;
\.


--
-- Data for Name: client_node_registrations; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client_node_registrations (client_id, value, name) FROM stdin;
\.


--
-- Data for Name: client_scope; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client_scope (id, name, realm_id, description, protocol) FROM stdin;
58912aa2-9f91-44c0-9d96-e9712da49547	offline_access	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect built-in scope: offline_access	openid-connect
deb190e9-b3f3-4987-b52e-b2ce1268583f	role_list	950f7f4b-1af6-4a64-bb5e-2561faa87127	SAML role list	saml
a097f9f9-5c79-4eba-af18-3cb6decdbb85	saml_organization	950f7f4b-1af6-4a64-bb5e-2561faa87127	Organization Membership	saml
ca6c61aa-bede-45fd-a52e-a4a548fb7068	profile	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect built-in scope: profile	openid-connect
f09ae408-44af-4145-9086-0acc4d9b4011	email	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect built-in scope: email	openid-connect
49bc6ebb-b477-4cc4-bd82-640d26338406	address	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect built-in scope: address	openid-connect
43e08f49-41f4-4130-bf7e-2e35a36b717c	phone	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect built-in scope: phone	openid-connect
4122c099-936e-4fcf-b236-1fda2083964b	roles	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect scope for add user roles to the access token	openid-connect
22117671-8539-42ba-8f4e-3c9422720fab	web-origins	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect scope for add allowed web origins to the access token	openid-connect
a3f1a812-5c5a-43d4-8ba5-08bba228eb17	microprofile-jwt	950f7f4b-1af6-4a64-bb5e-2561faa87127	Microprofile - JWT built-in scope	openid-connect
3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	acr	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect scope for add acr (authentication context class reference) to the token	openid-connect
09399803-e66a-4dd8-ab13-23b721d1a2e9	basic	950f7f4b-1af6-4a64-bb5e-2561faa87127	OpenID Connect scope for add all basic claims to the token	openid-connect
48078758-f8c1-4b6c-bffe-93addc0eeeb5	service_account	950f7f4b-1af6-4a64-bb5e-2561faa87127	Specific scope for a client enabled for service accounts	openid-connect
b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	organization	950f7f4b-1af6-4a64-bb5e-2561faa87127	Additional claims about the organization a subject belongs to	openid-connect
c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	organization	c55a12d3-a06b-43f4-b990-28390a55a7af	Additional claims about the organization a subject belongs to	openid-connect
37506bdf-0373-4b65-81f0-97fcd9c8a32f	role_list	c55a12d3-a06b-43f4-b990-28390a55a7af	SAML role list	saml
ccae089a-7026-46a2-941d-cd676ef19750	web-origins	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect scope for add allowed web origins to the access token	openid-connect
153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	roles	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect scope for add user roles to the access token	openid-connect
045de1b1-5274-4d89-870d-ff589f80c2ff	microprofile-jwt	c55a12d3-a06b-43f4-b990-28390a55a7af	Microprofile - JWT built-in scope	openid-connect
d6e2a201-ae36-4402-981d-cd78cd93b451	basic	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect scope for add all basic claims to the token	openid-connect
11b465e1-9968-493c-b42c-ac582a714f76	offline_access	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect built-in scope: offline_access	openid-connect
ebc0e19e-d261-4423-b459-4f520f552fd8	profile	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect built-in scope: profile	openid-connect
430e79f6-80c8-4bc6-bc8d-b9fad89705c2	saml_organization	c55a12d3-a06b-43f4-b990-28390a55a7af	Organization Membership	saml
74994a75-496d-432f-88d9-dabb47c922b5	phone	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect built-in scope: phone	openid-connect
4bef3907-f963-4ce5-b727-a3b95e0c1e36	acr	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect scope for add acr (authentication context class reference) to the token	openid-connect
15bbb040-e553-4b52-9e80-47006803f558	service_account	c55a12d3-a06b-43f4-b990-28390a55a7af	Specific scope for a client enabled for service accounts	openid-connect
909551aa-cac1-4add-8051-eff0829dee3e	address	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect built-in scope: address	openid-connect
1f1b437f-5f85-4c68-9bfa-9d82130c5f08	email	c55a12d3-a06b-43f4-b990-28390a55a7af	OpenID Connect built-in scope: email	openid-connect
\.


--
-- Data for Name: client_scope_attributes; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client_scope_attributes (scope_id, value, name) FROM stdin;
58912aa2-9f91-44c0-9d96-e9712da49547	true	display.on.consent.screen
58912aa2-9f91-44c0-9d96-e9712da49547	${offlineAccessScopeConsentText}	consent.screen.text
deb190e9-b3f3-4987-b52e-b2ce1268583f	true	display.on.consent.screen
deb190e9-b3f3-4987-b52e-b2ce1268583f	${samlRoleListScopeConsentText}	consent.screen.text
a097f9f9-5c79-4eba-af18-3cb6decdbb85	false	display.on.consent.screen
ca6c61aa-bede-45fd-a52e-a4a548fb7068	true	display.on.consent.screen
ca6c61aa-bede-45fd-a52e-a4a548fb7068	${profileScopeConsentText}	consent.screen.text
ca6c61aa-bede-45fd-a52e-a4a548fb7068	true	include.in.token.scope
f09ae408-44af-4145-9086-0acc4d9b4011	true	display.on.consent.screen
f09ae408-44af-4145-9086-0acc4d9b4011	${emailScopeConsentText}	consent.screen.text
f09ae408-44af-4145-9086-0acc4d9b4011	true	include.in.token.scope
49bc6ebb-b477-4cc4-bd82-640d26338406	true	display.on.consent.screen
49bc6ebb-b477-4cc4-bd82-640d26338406	${addressScopeConsentText}	consent.screen.text
49bc6ebb-b477-4cc4-bd82-640d26338406	true	include.in.token.scope
43e08f49-41f4-4130-bf7e-2e35a36b717c	true	display.on.consent.screen
43e08f49-41f4-4130-bf7e-2e35a36b717c	${phoneScopeConsentText}	consent.screen.text
43e08f49-41f4-4130-bf7e-2e35a36b717c	true	include.in.token.scope
4122c099-936e-4fcf-b236-1fda2083964b	true	display.on.consent.screen
4122c099-936e-4fcf-b236-1fda2083964b	${rolesScopeConsentText}	consent.screen.text
4122c099-936e-4fcf-b236-1fda2083964b	false	include.in.token.scope
22117671-8539-42ba-8f4e-3c9422720fab	false	display.on.consent.screen
22117671-8539-42ba-8f4e-3c9422720fab		consent.screen.text
22117671-8539-42ba-8f4e-3c9422720fab	false	include.in.token.scope
a3f1a812-5c5a-43d4-8ba5-08bba228eb17	false	display.on.consent.screen
a3f1a812-5c5a-43d4-8ba5-08bba228eb17	true	include.in.token.scope
3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	false	display.on.consent.screen
3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	false	include.in.token.scope
09399803-e66a-4dd8-ab13-23b721d1a2e9	false	display.on.consent.screen
09399803-e66a-4dd8-ab13-23b721d1a2e9	false	include.in.token.scope
48078758-f8c1-4b6c-bffe-93addc0eeeb5	false	display.on.consent.screen
48078758-f8c1-4b6c-bffe-93addc0eeeb5	false	include.in.token.scope
b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	true	display.on.consent.screen
b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	${organizationScopeConsentText}	consent.screen.text
b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	true	include.in.token.scope
c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	true	include.in.token.scope
c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	${organizationScopeConsentText}	consent.screen.text
c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	true	display.on.consent.screen
37506bdf-0373-4b65-81f0-97fcd9c8a32f	${samlRoleListScopeConsentText}	consent.screen.text
37506bdf-0373-4b65-81f0-97fcd9c8a32f	true	display.on.consent.screen
ccae089a-7026-46a2-941d-cd676ef19750	false	include.in.token.scope
ccae089a-7026-46a2-941d-cd676ef19750		consent.screen.text
ccae089a-7026-46a2-941d-cd676ef19750	false	display.on.consent.screen
153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	false	include.in.token.scope
153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	${rolesScopeConsentText}	consent.screen.text
153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	true	display.on.consent.screen
045de1b1-5274-4d89-870d-ff589f80c2ff	true	include.in.token.scope
045de1b1-5274-4d89-870d-ff589f80c2ff	false	display.on.consent.screen
d6e2a201-ae36-4402-981d-cd78cd93b451	false	include.in.token.scope
d6e2a201-ae36-4402-981d-cd78cd93b451	false	display.on.consent.screen
11b465e1-9968-493c-b42c-ac582a714f76	${offlineAccessScopeConsentText}	consent.screen.text
11b465e1-9968-493c-b42c-ac582a714f76	true	display.on.consent.screen
ebc0e19e-d261-4423-b459-4f520f552fd8	true	include.in.token.scope
ebc0e19e-d261-4423-b459-4f520f552fd8	${profileScopeConsentText}	consent.screen.text
ebc0e19e-d261-4423-b459-4f520f552fd8	true	display.on.consent.screen
430e79f6-80c8-4bc6-bc8d-b9fad89705c2	false	display.on.consent.screen
74994a75-496d-432f-88d9-dabb47c922b5	true	include.in.token.scope
74994a75-496d-432f-88d9-dabb47c922b5	${phoneScopeConsentText}	consent.screen.text
74994a75-496d-432f-88d9-dabb47c922b5	true	display.on.consent.screen
4bef3907-f963-4ce5-b727-a3b95e0c1e36	false	include.in.token.scope
4bef3907-f963-4ce5-b727-a3b95e0c1e36	false	display.on.consent.screen
15bbb040-e553-4b52-9e80-47006803f558	false	include.in.token.scope
15bbb040-e553-4b52-9e80-47006803f558	false	display.on.consent.screen
909551aa-cac1-4add-8051-eff0829dee3e	true	include.in.token.scope
909551aa-cac1-4add-8051-eff0829dee3e	${addressScopeConsentText}	consent.screen.text
909551aa-cac1-4add-8051-eff0829dee3e	true	display.on.consent.screen
1f1b437f-5f85-4c68-9bfa-9d82130c5f08	true	include.in.token.scope
1f1b437f-5f85-4c68-9bfa-9d82130c5f08	${emailScopeConsentText}	consent.screen.text
1f1b437f-5f85-4c68-9bfa-9d82130c5f08	true	display.on.consent.screen
\.


--
-- Data for Name: client_scope_client; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client_scope_client (client_id, scope_id, default_scope) FROM stdin;
70f8e924-f945-4a2a-b7f2-130505a5f8f7	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	t
70f8e924-f945-4a2a-b7f2-130505a5f8f7	09399803-e66a-4dd8-ab13-23b721d1a2e9	t
70f8e924-f945-4a2a-b7f2-130505a5f8f7	ca6c61aa-bede-45fd-a52e-a4a548fb7068	t
70f8e924-f945-4a2a-b7f2-130505a5f8f7	f09ae408-44af-4145-9086-0acc4d9b4011	t
70f8e924-f945-4a2a-b7f2-130505a5f8f7	4122c099-936e-4fcf-b236-1fda2083964b	t
70f8e924-f945-4a2a-b7f2-130505a5f8f7	22117671-8539-42ba-8f4e-3c9422720fab	t
70f8e924-f945-4a2a-b7f2-130505a5f8f7	58912aa2-9f91-44c0-9d96-e9712da49547	f
70f8e924-f945-4a2a-b7f2-130505a5f8f7	43e08f49-41f4-4130-bf7e-2e35a36b717c	f
70f8e924-f945-4a2a-b7f2-130505a5f8f7	49bc6ebb-b477-4cc4-bd82-640d26338406	f
70f8e924-f945-4a2a-b7f2-130505a5f8f7	a3f1a812-5c5a-43d4-8ba5-08bba228eb17	f
70f8e924-f945-4a2a-b7f2-130505a5f8f7	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	f
640d1fae-9a47-46dc-81d3-8ed39870984a	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	t
640d1fae-9a47-46dc-81d3-8ed39870984a	09399803-e66a-4dd8-ab13-23b721d1a2e9	t
640d1fae-9a47-46dc-81d3-8ed39870984a	ca6c61aa-bede-45fd-a52e-a4a548fb7068	t
640d1fae-9a47-46dc-81d3-8ed39870984a	f09ae408-44af-4145-9086-0acc4d9b4011	t
640d1fae-9a47-46dc-81d3-8ed39870984a	4122c099-936e-4fcf-b236-1fda2083964b	t
640d1fae-9a47-46dc-81d3-8ed39870984a	22117671-8539-42ba-8f4e-3c9422720fab	t
640d1fae-9a47-46dc-81d3-8ed39870984a	58912aa2-9f91-44c0-9d96-e9712da49547	f
640d1fae-9a47-46dc-81d3-8ed39870984a	43e08f49-41f4-4130-bf7e-2e35a36b717c	f
640d1fae-9a47-46dc-81d3-8ed39870984a	49bc6ebb-b477-4cc4-bd82-640d26338406	f
640d1fae-9a47-46dc-81d3-8ed39870984a	a3f1a812-5c5a-43d4-8ba5-08bba228eb17	f
640d1fae-9a47-46dc-81d3-8ed39870984a	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	f
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	t
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	09399803-e66a-4dd8-ab13-23b721d1a2e9	t
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	ca6c61aa-bede-45fd-a52e-a4a548fb7068	t
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	f09ae408-44af-4145-9086-0acc4d9b4011	t
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	4122c099-936e-4fcf-b236-1fda2083964b	t
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	22117671-8539-42ba-8f4e-3c9422720fab	t
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	58912aa2-9f91-44c0-9d96-e9712da49547	f
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	43e08f49-41f4-4130-bf7e-2e35a36b717c	f
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	49bc6ebb-b477-4cc4-bd82-640d26338406	f
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	a3f1a812-5c5a-43d4-8ba5-08bba228eb17	f
b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	f
4af7bbb0-5dbf-4fdd-b730-79b146a12050	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	t
4af7bbb0-5dbf-4fdd-b730-79b146a12050	09399803-e66a-4dd8-ab13-23b721d1a2e9	t
4af7bbb0-5dbf-4fdd-b730-79b146a12050	ca6c61aa-bede-45fd-a52e-a4a548fb7068	t
4af7bbb0-5dbf-4fdd-b730-79b146a12050	f09ae408-44af-4145-9086-0acc4d9b4011	t
4af7bbb0-5dbf-4fdd-b730-79b146a12050	4122c099-936e-4fcf-b236-1fda2083964b	t
4af7bbb0-5dbf-4fdd-b730-79b146a12050	22117671-8539-42ba-8f4e-3c9422720fab	t
4af7bbb0-5dbf-4fdd-b730-79b146a12050	58912aa2-9f91-44c0-9d96-e9712da49547	f
4af7bbb0-5dbf-4fdd-b730-79b146a12050	43e08f49-41f4-4130-bf7e-2e35a36b717c	f
4af7bbb0-5dbf-4fdd-b730-79b146a12050	49bc6ebb-b477-4cc4-bd82-640d26338406	f
4af7bbb0-5dbf-4fdd-b730-79b146a12050	a3f1a812-5c5a-43d4-8ba5-08bba228eb17	f
4af7bbb0-5dbf-4fdd-b730-79b146a12050	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	f
a8ce899c-8a3d-4391-98dc-72610c85b515	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	t
a8ce899c-8a3d-4391-98dc-72610c85b515	09399803-e66a-4dd8-ab13-23b721d1a2e9	t
a8ce899c-8a3d-4391-98dc-72610c85b515	ca6c61aa-bede-45fd-a52e-a4a548fb7068	t
a8ce899c-8a3d-4391-98dc-72610c85b515	f09ae408-44af-4145-9086-0acc4d9b4011	t
a8ce899c-8a3d-4391-98dc-72610c85b515	4122c099-936e-4fcf-b236-1fda2083964b	t
a8ce899c-8a3d-4391-98dc-72610c85b515	22117671-8539-42ba-8f4e-3c9422720fab	t
a8ce899c-8a3d-4391-98dc-72610c85b515	58912aa2-9f91-44c0-9d96-e9712da49547	f
a8ce899c-8a3d-4391-98dc-72610c85b515	43e08f49-41f4-4130-bf7e-2e35a36b717c	f
a8ce899c-8a3d-4391-98dc-72610c85b515	49bc6ebb-b477-4cc4-bd82-640d26338406	f
a8ce899c-8a3d-4391-98dc-72610c85b515	a3f1a812-5c5a-43d4-8ba5-08bba228eb17	f
a8ce899c-8a3d-4391-98dc-72610c85b515	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	f
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	t
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	09399803-e66a-4dd8-ab13-23b721d1a2e9	t
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	ca6c61aa-bede-45fd-a52e-a4a548fb7068	t
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	f09ae408-44af-4145-9086-0acc4d9b4011	t
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	4122c099-936e-4fcf-b236-1fda2083964b	t
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	22117671-8539-42ba-8f4e-3c9422720fab	t
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	58912aa2-9f91-44c0-9d96-e9712da49547	f
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	43e08f49-41f4-4130-bf7e-2e35a36b717c	f
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	49bc6ebb-b477-4cc4-bd82-640d26338406	f
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	a3f1a812-5c5a-43d4-8ba5-08bba228eb17	f
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	f
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	ebc0e19e-d261-4423-b459-4f520f552fd8	t
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	ccae089a-7026-46a2-941d-cd676ef19750	t
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	t
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	4bef3907-f963-4ce5-b727-a3b95e0c1e36	t
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	d6e2a201-ae36-4402-981d-cd78cd93b451	t
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	1f1b437f-5f85-4c68-9bfa-9d82130c5f08	t
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	f
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	74994a75-496d-432f-88d9-dabb47c922b5	f
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	045de1b1-5274-4d89-870d-ff589f80c2ff	f
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	909551aa-cac1-4add-8051-eff0829dee3e	f
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	11b465e1-9968-493c-b42c-ac582a714f76	f
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	ebc0e19e-d261-4423-b459-4f520f552fd8	t
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	ccae089a-7026-46a2-941d-cd676ef19750	t
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	t
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	4bef3907-f963-4ce5-b727-a3b95e0c1e36	t
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	d6e2a201-ae36-4402-981d-cd78cd93b451	t
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	1f1b437f-5f85-4c68-9bfa-9d82130c5f08	t
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	f
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	74994a75-496d-432f-88d9-dabb47c922b5	f
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	045de1b1-5274-4d89-870d-ff589f80c2ff	f
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	909551aa-cac1-4add-8051-eff0829dee3e	f
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	11b465e1-9968-493c-b42c-ac582a714f76	f
3f723df7-fc18-4a13-9a0b-3df75da808d7	ebc0e19e-d261-4423-b459-4f520f552fd8	t
3f723df7-fc18-4a13-9a0b-3df75da808d7	ccae089a-7026-46a2-941d-cd676ef19750	t
3f723df7-fc18-4a13-9a0b-3df75da808d7	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	t
3f723df7-fc18-4a13-9a0b-3df75da808d7	4bef3907-f963-4ce5-b727-a3b95e0c1e36	t
3f723df7-fc18-4a13-9a0b-3df75da808d7	d6e2a201-ae36-4402-981d-cd78cd93b451	t
3f723df7-fc18-4a13-9a0b-3df75da808d7	1f1b437f-5f85-4c68-9bfa-9d82130c5f08	t
3f723df7-fc18-4a13-9a0b-3df75da808d7	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	f
3f723df7-fc18-4a13-9a0b-3df75da808d7	74994a75-496d-432f-88d9-dabb47c922b5	f
3f723df7-fc18-4a13-9a0b-3df75da808d7	045de1b1-5274-4d89-870d-ff589f80c2ff	f
3f723df7-fc18-4a13-9a0b-3df75da808d7	909551aa-cac1-4add-8051-eff0829dee3e	f
3f723df7-fc18-4a13-9a0b-3df75da808d7	11b465e1-9968-493c-b42c-ac582a714f76	f
b141edca-aa19-47f5-87be-23de76c8a44f	ebc0e19e-d261-4423-b459-4f520f552fd8	t
b141edca-aa19-47f5-87be-23de76c8a44f	ccae089a-7026-46a2-941d-cd676ef19750	t
b141edca-aa19-47f5-87be-23de76c8a44f	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	t
b141edca-aa19-47f5-87be-23de76c8a44f	4bef3907-f963-4ce5-b727-a3b95e0c1e36	t
b141edca-aa19-47f5-87be-23de76c8a44f	d6e2a201-ae36-4402-981d-cd78cd93b451	t
b141edca-aa19-47f5-87be-23de76c8a44f	1f1b437f-5f85-4c68-9bfa-9d82130c5f08	t
b141edca-aa19-47f5-87be-23de76c8a44f	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	f
b141edca-aa19-47f5-87be-23de76c8a44f	74994a75-496d-432f-88d9-dabb47c922b5	f
b141edca-aa19-47f5-87be-23de76c8a44f	045de1b1-5274-4d89-870d-ff589f80c2ff	f
b141edca-aa19-47f5-87be-23de76c8a44f	909551aa-cac1-4add-8051-eff0829dee3e	f
b141edca-aa19-47f5-87be-23de76c8a44f	11b465e1-9968-493c-b42c-ac582a714f76	f
83ab17ea-566c-43b4-abc5-847346d7485a	ebc0e19e-d261-4423-b459-4f520f552fd8	t
83ab17ea-566c-43b4-abc5-847346d7485a	ccae089a-7026-46a2-941d-cd676ef19750	t
83ab17ea-566c-43b4-abc5-847346d7485a	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	t
83ab17ea-566c-43b4-abc5-847346d7485a	4bef3907-f963-4ce5-b727-a3b95e0c1e36	t
83ab17ea-566c-43b4-abc5-847346d7485a	d6e2a201-ae36-4402-981d-cd78cd93b451	t
83ab17ea-566c-43b4-abc5-847346d7485a	1f1b437f-5f85-4c68-9bfa-9d82130c5f08	t
83ab17ea-566c-43b4-abc5-847346d7485a	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	f
83ab17ea-566c-43b4-abc5-847346d7485a	74994a75-496d-432f-88d9-dabb47c922b5	f
83ab17ea-566c-43b4-abc5-847346d7485a	045de1b1-5274-4d89-870d-ff589f80c2ff	f
83ab17ea-566c-43b4-abc5-847346d7485a	909551aa-cac1-4add-8051-eff0829dee3e	f
83ab17ea-566c-43b4-abc5-847346d7485a	11b465e1-9968-493c-b42c-ac582a714f76	t
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	ebc0e19e-d261-4423-b459-4f520f552fd8	t
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	ccae089a-7026-46a2-941d-cd676ef19750	t
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	t
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	4bef3907-f963-4ce5-b727-a3b95e0c1e36	t
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	d6e2a201-ae36-4402-981d-cd78cd93b451	t
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	1f1b437f-5f85-4c68-9bfa-9d82130c5f08	t
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	f
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	74994a75-496d-432f-88d9-dabb47c922b5	f
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	045de1b1-5274-4d89-870d-ff589f80c2ff	f
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	909551aa-cac1-4add-8051-eff0829dee3e	f
1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	11b465e1-9968-493c-b42c-ac582a714f76	f
043917f3-a51e-4661-83c1-41b19f4ee3fe	ebc0e19e-d261-4423-b459-4f520f552fd8	t
043917f3-a51e-4661-83c1-41b19f4ee3fe	ccae089a-7026-46a2-941d-cd676ef19750	t
043917f3-a51e-4661-83c1-41b19f4ee3fe	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	t
043917f3-a51e-4661-83c1-41b19f4ee3fe	4bef3907-f963-4ce5-b727-a3b95e0c1e36	t
043917f3-a51e-4661-83c1-41b19f4ee3fe	d6e2a201-ae36-4402-981d-cd78cd93b451	t
043917f3-a51e-4661-83c1-41b19f4ee3fe	1f1b437f-5f85-4c68-9bfa-9d82130c5f08	t
043917f3-a51e-4661-83c1-41b19f4ee3fe	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	f
043917f3-a51e-4661-83c1-41b19f4ee3fe	74994a75-496d-432f-88d9-dabb47c922b5	f
043917f3-a51e-4661-83c1-41b19f4ee3fe	045de1b1-5274-4d89-870d-ff589f80c2ff	f
043917f3-a51e-4661-83c1-41b19f4ee3fe	909551aa-cac1-4add-8051-eff0829dee3e	f
043917f3-a51e-4661-83c1-41b19f4ee3fe	11b465e1-9968-493c-b42c-ac582a714f76	f
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	t
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	09399803-e66a-4dd8-ab13-23b721d1a2e9	t
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	ca6c61aa-bede-45fd-a52e-a4a548fb7068	t
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	f09ae408-44af-4145-9086-0acc4d9b4011	t
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	4122c099-936e-4fcf-b236-1fda2083964b	t
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	22117671-8539-42ba-8f4e-3c9422720fab	t
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	58912aa2-9f91-44c0-9d96-e9712da49547	f
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	43e08f49-41f4-4130-bf7e-2e35a36b717c	f
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	49bc6ebb-b477-4cc4-bd82-640d26338406	f
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	a3f1a812-5c5a-43d4-8ba5-08bba228eb17	f
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	f
b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	48078758-f8c1-4b6c-bffe-93addc0eeeb5	t
\.


--
-- Data for Name: client_scope_role_mapping; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.client_scope_role_mapping (scope_id, role_id) FROM stdin;
58912aa2-9f91-44c0-9d96-e9712da49547	c5c2e4d7-4e88-4aa8-981c-4984a37ec40b
11b465e1-9968-493c-b42c-ac582a714f76	abd702be-194e-420f-9a46-821e6340a8dd
\.


--
-- Data for Name: component; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.component (id, name, parent_id, provider_id, provider_type, realm_id, sub_type) FROM stdin;
b03c9307-6114-4bdb-8015-d6d97c4a2571	Trusted Hosts	950f7f4b-1af6-4a64-bb5e-2561faa87127	trusted-hosts	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	anonymous
af09a1ac-e568-45a6-9e67-d96a26010fda	Consent Required	950f7f4b-1af6-4a64-bb5e-2561faa87127	consent-required	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	anonymous
85de1ed9-21f9-4004-afac-95a0b32301ec	Full Scope Disabled	950f7f4b-1af6-4a64-bb5e-2561faa87127	scope	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	anonymous
2930eed2-a4f3-46f7-9970-43c91e793de6	Max Clients Limit	950f7f4b-1af6-4a64-bb5e-2561faa87127	max-clients	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	anonymous
6235154b-e9c5-4d17-85e3-4563b4e829bc	Allowed Protocol Mapper Types	950f7f4b-1af6-4a64-bb5e-2561faa87127	allowed-protocol-mappers	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	anonymous
3e325f55-f710-4aad-a2a3-bedc64fd35d7	Allowed Client Scopes	950f7f4b-1af6-4a64-bb5e-2561faa87127	allowed-client-templates	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	anonymous
4204bb77-c05a-42ad-982c-455da39d8b2b	Allowed Registration Web Origins	950f7f4b-1af6-4a64-bb5e-2561faa87127	registration-web-origins	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	anonymous
4d16f243-5c8d-4f7f-a59c-9c0321367d3b	Allowed Protocol Mapper Types	950f7f4b-1af6-4a64-bb5e-2561faa87127	allowed-protocol-mappers	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	authenticated
188a79da-df92-462f-8b41-e6b0bec66fb2	Allowed Client Scopes	950f7f4b-1af6-4a64-bb5e-2561faa87127	allowed-client-templates	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	authenticated
4ae0e478-0d50-4de9-b327-2337c11de288	Allowed Registration Web Origins	950f7f4b-1af6-4a64-bb5e-2561faa87127	registration-web-origins	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	authenticated
76f3ae0a-d01b-4cd5-8e0d-44f738923c92	rsa-generated	950f7f4b-1af6-4a64-bb5e-2561faa87127	rsa-generated	org.keycloak.keys.KeyProvider	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N
1720d20f-23a0-4d19-b1a7-e408ae161b34	rsa-enc-generated	950f7f4b-1af6-4a64-bb5e-2561faa87127	rsa-enc-generated	org.keycloak.keys.KeyProvider	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N
e2440177-15be-4bb2-9e6e-07a479420650	hmac-generated-hs512	950f7f4b-1af6-4a64-bb5e-2561faa87127	hmac-generated	org.keycloak.keys.KeyProvider	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N
95e4f666-d3d8-48c0-874a-dbab75d5ead8	aes-generated	950f7f4b-1af6-4a64-bb5e-2561faa87127	aes-generated	org.keycloak.keys.KeyProvider	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N
0dc316c4-7be2-46cf-80c1-400b1142c142	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	declarative-user-profile	org.keycloak.userprofile.UserProfileProvider	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N
0435310e-2b98-4960-9aec-a8425901ee1e	Allowed Client Scopes	c55a12d3-a06b-43f4-b990-28390a55a7af	allowed-client-templates	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	anonymous
2497eb6c-8552-49e6-a159-493bac003a54	Allowed Protocol Mapper Types	c55a12d3-a06b-43f4-b990-28390a55a7af	allowed-protocol-mappers	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	authenticated
2baf6124-d931-4482-bb64-76ab445c7667	Allowed Client Scopes	c55a12d3-a06b-43f4-b990-28390a55a7af	allowed-client-templates	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	authenticated
a8a74107-2a1b-4d5b-a0a9-7de26c27b421	Max Clients Limit	c55a12d3-a06b-43f4-b990-28390a55a7af	max-clients	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	anonymous
fb651779-98da-4e18-8db8-d184e606a4eb	Consent Required	c55a12d3-a06b-43f4-b990-28390a55a7af	consent-required	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	anonymous
1be1f438-1208-45fa-bac7-44ddba7abeb3	Allowed Protocol Mapper Types	c55a12d3-a06b-43f4-b990-28390a55a7af	allowed-protocol-mappers	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	anonymous
dd78c320-42a6-4334-a82b-c74a8a72671a	Trusted Hosts	c55a12d3-a06b-43f4-b990-28390a55a7af	trusted-hosts	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	anonymous
e85d4fb9-098c-4bf9-8cb8-4c0cfc6aac1a	Full Scope Disabled	c55a12d3-a06b-43f4-b990-28390a55a7af	scope	org.keycloak.services.clientregistration.policy.ClientRegistrationPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	anonymous
06fb3851-85c9-489e-81e0-37830c3bf2a2	rsa-generated	c55a12d3-a06b-43f4-b990-28390a55a7af	rsa-generated	org.keycloak.keys.KeyProvider	c55a12d3-a06b-43f4-b990-28390a55a7af	\N
3bfb7310-7d80-4919-9970-f3be9b30ab4c	rsa-enc-generated	c55a12d3-a06b-43f4-b990-28390a55a7af	rsa-enc-generated	org.keycloak.keys.KeyProvider	c55a12d3-a06b-43f4-b990-28390a55a7af	\N
42739c0e-d602-4f60-a82e-dee3b9234805	hmac-generated-hs512	c55a12d3-a06b-43f4-b990-28390a55a7af	hmac-generated	org.keycloak.keys.KeyProvider	c55a12d3-a06b-43f4-b990-28390a55a7af	\N
9b4c06b1-2135-42c9-add1-43122569209b	aes-generated	c55a12d3-a06b-43f4-b990-28390a55a7af	aes-generated	org.keycloak.keys.KeyProvider	c55a12d3-a06b-43f4-b990-28390a55a7af	\N
\.


--
-- Data for Name: component_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.component_config (id, component_id, name, value) FROM stdin;
0134a743-e2b2-4c6c-a72b-510311914863	b03c9307-6114-4bdb-8015-d6d97c4a2571	host-sending-registration-request-must-match	true
7b6d1c63-05c4-4ca4-88cb-2cbc2290e0fe	b03c9307-6114-4bdb-8015-d6d97c4a2571	client-uris-must-match	true
a83bfcde-8122-42e3-a531-62e6c39a6a0a	6235154b-e9c5-4d17-85e3-4563b4e829bc	allowed-protocol-mapper-types	saml-user-attribute-mapper
e6ea25f2-0893-4bc8-acd8-cd35431f6126	6235154b-e9c5-4d17-85e3-4563b4e829bc	allowed-protocol-mapper-types	saml-role-list-mapper
f3557d87-de63-4ce3-96c1-aa01047d86d4	6235154b-e9c5-4d17-85e3-4563b4e829bc	allowed-protocol-mapper-types	oidc-address-mapper
67d28923-9447-4f49-9c62-5c55372b3969	6235154b-e9c5-4d17-85e3-4563b4e829bc	allowed-protocol-mapper-types	oidc-sha256-pairwise-sub-mapper
f97cb005-5765-4a0c-b1b6-ea7ee05c20b9	6235154b-e9c5-4d17-85e3-4563b4e829bc	allowed-protocol-mapper-types	saml-user-property-mapper
6345e354-bc49-4f2d-8cef-457799e34896	6235154b-e9c5-4d17-85e3-4563b4e829bc	allowed-protocol-mapper-types	oidc-usermodel-property-mapper
ec3f5d1f-b219-4adb-b1d9-0cd7e046e226	6235154b-e9c5-4d17-85e3-4563b4e829bc	allowed-protocol-mapper-types	oidc-usermodel-attribute-mapper
c5ef8558-2400-4929-9705-cc65679a9ffb	6235154b-e9c5-4d17-85e3-4563b4e829bc	allowed-protocol-mapper-types	oidc-full-name-mapper
511ff0d0-d0c8-4151-900a-5d242a2e76f1	2930eed2-a4f3-46f7-9970-43c91e793de6	max-clients	200
a8b6b0e1-4179-4c21-a103-8b78301bf033	4d16f243-5c8d-4f7f-a59c-9c0321367d3b	allowed-protocol-mapper-types	saml-user-attribute-mapper
04e0969b-41fc-4602-82d3-4324efc07b15	4d16f243-5c8d-4f7f-a59c-9c0321367d3b	allowed-protocol-mapper-types	oidc-address-mapper
a31c0883-1ceb-436f-afe0-9c7df068fa96	4d16f243-5c8d-4f7f-a59c-9c0321367d3b	allowed-protocol-mapper-types	oidc-sha256-pairwise-sub-mapper
4fb73c16-6bdf-4a4f-8986-fedb80703e90	4d16f243-5c8d-4f7f-a59c-9c0321367d3b	allowed-protocol-mapper-types	oidc-usermodel-property-mapper
189736bb-8d29-45fb-a82b-eb123f95bb0f	4d16f243-5c8d-4f7f-a59c-9c0321367d3b	allowed-protocol-mapper-types	saml-user-property-mapper
8ab7a704-5d07-42c9-b5b4-273c039810eb	4d16f243-5c8d-4f7f-a59c-9c0321367d3b	allowed-protocol-mapper-types	oidc-full-name-mapper
5d0c65ec-ab49-4a5a-919e-91f19b2537f3	4d16f243-5c8d-4f7f-a59c-9c0321367d3b	allowed-protocol-mapper-types	saml-role-list-mapper
b37f297b-6818-4f18-bab4-ca5ca4394787	4d16f243-5c8d-4f7f-a59c-9c0321367d3b	allowed-protocol-mapper-types	oidc-usermodel-attribute-mapper
fc28b625-3aa9-4280-a382-ee4f03784149	188a79da-df92-462f-8b41-e6b0bec66fb2	allow-default-scopes	true
e80e453e-b813-4a20-826f-e442eb005c5f	3e325f55-f710-4aad-a2a3-bedc64fd35d7	allow-default-scopes	true
618a1b4d-3645-47a9-8b71-e9238f093c66	76f3ae0a-d01b-4cd5-8e0d-44f738923c92	certificate	MIICmzCCAYMCBgGd3tZQZTANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZtYXN0ZXIwHhcNMjYwNDMwMTQzOTQwWhcNMzYwNDMwMTQ0MTIwWjARMQ8wDQYDVQQDDAZtYXN0ZXIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCxSx+JtQxbrMMLZE+shks3SUxlTlGZvSSxH+HldeR60J91HhL7ehTB/vjMDZNAFCTpP3wtYS3+2PEBG0tNa61BHSkSy2tII1GA2dd9Zxw4AyrEHkYs0gT/IdpyM7ef5fpkMsv56R+LM93BbF9aOuFmskVkfZbJqO9oHU9tH8qnKCNenNf3OqJrZ+yS3ZU/DaPZoSmIo9FFxKxnjRUauzZx44bg+hblxkCOFC00tj6AI41HEyLwANOnEABo7z8Zdr2WFZE127J5IHPsAd2wyUHpL0KIeu1tj2aXENEF+odziL4wv6iaCYqm0/lFq2QGtZ4xJHsXrzziXzy3gGF5GEo1AgMBAAEwDQYJKoZIhvcNAQELBQADggEBAAHmNURZXK/x75c7osxHHHP5924HiZA5byX9IeophHxcYX81Yd5yT+qGZPFLw1ugOwYQwajgQFvt+DjQi72JB5WoGx5uEL7heaAGGSkzYrQTOqxx0oFx8UgEp3/J3NaRkbmFzwriRwzrkEW8cNN/ItAA4Iq2bbrLlfz2TFQDGKrtOvmZZfyBPsmNogvyhATwN3EoqvbAy+gTDTPMJ/Q7sJjfLnpzjotc0BNHN5SeniuQOM5Z5wrirUJd8SbO3AL3BHvH2/XP6rsLAHcapxRx+8QtT4RoPc5zsaT+n6C9d5x8tUYjbLYWw3I7lx0n0KypWqg5Qsd1JXeUhvpaAwrRUF8=
79fbc4ad-fc15-4962-907d-f07d81727160	76f3ae0a-d01b-4cd5-8e0d-44f738923c92	keyUse	SIG
a699efe7-96dc-4ad8-9f6a-cc0aeb915622	76f3ae0a-d01b-4cd5-8e0d-44f738923c92	priority	100
ef945ba5-d9a6-444c-ba6f-b70acbd7f3b6	76f3ae0a-d01b-4cd5-8e0d-44f738923c92	privateKey	MIIEoQIBAAKCAQEAsUsfibUMW6zDC2RPrIZLN0lMZU5Rmb0ksR/h5XXketCfdR4S+3oUwf74zA2TQBQk6T98LWEt/tjxARtLTWutQR0pEstrSCNRgNnXfWccOAMqxB5GLNIE/yHacjO3n+X6ZDLL+ekfizPdwWxfWjrhZrJFZH2WyajvaB1PbR/KpygjXpzX9zqia2fskt2VPw2j2aEpiKPRRcSsZ40VGrs2ceOG4PoW5cZAjhQtNLY+gCONRxMi8ADTpxAAaO8/GXa9lhWRNduyeSBz7AHdsMlB6S9CiHrtbY9mlxDRBfqHc4i+ML+omgmKptP5RatkBrWeMSR7F6884l88t4BheRhKNQIDAQABAoH/BHNVYz9R6Ghf7irEHLBYKRkFQwq6Nz+IQRmjmf1B1N1X8cZWcC09IpOpLDCwApZy9YPCNwYfsFfpfU0//d0zIOhe8+wvQkUJ4Id/lefJJtxSs4fDnHJACSWM7xF3FXyamuNaL5CK0P2r8qoZH+FMnYjWJTqOwBIOb3bT1vlOofldJaV9aSERgXS7iyoMS66d7eVtUtqpeSj35TbJCVMFT8hvqUNnIcvmPg+EcczRk8IytGB3tK+dhAy3T7o+Ej1++lubTJl/6eNm7hfEt6oiEdYZ7fZHzOXlt9NefS9D4MB9gpdkrYHwVc8jU8vdQSEVrcrYdL/QtQkNx/Yir+WBAoGBAO10TV3b73fjGD6JIsfY/F+OBZltLFgaglrqvuarWo8IyUvRD/OPj2WvcW54mb8ZcOFK2AWHwSG7HAzfEJaN0eFyMr7WW6jXCILrTMTnV+pXHtEJAQwOGU2yHOZDleItApufsUs1UcVBnSxmLg+CvGbjVt6S5ahO2PV7jzd/EiVVAoGBAL8j9KMQh3I1CzSxgZLvHqHnftq6G7Y9KBRMeGSwzTzcYva5r7FjlLdZ5g+XYRFCu6AE0+hl1fP+25UsO8ca2P5fcL6u/CkRP9zBc0oIe56uxCbUWIBMnZ9i3P1p8RBovUHRH33nlkEBUfZgGQ4/XkZb9xmSJjjlv/kBlf3rx5FhAoGBAI17k7GOH1Q2qrZwLZoYLt+clreBNj/Uo8EaR97XUKETIiWbjr6X1mBHNfYVw736oaiLWMWKyseXXjJJIvAh1mFXEudkf77NSVQAcYCNO3P0rvbsP4R4ThlePBvzPzZBjWE+uHvQbEV1P/o5c85oHmvLn3IE4vPy7xDtqzrs6tn1AoGAX+4vzddx40P0B9I+8fvJKAEDjctyNRikkOuAUSjbGPyTPrkbELCl5w/bg1+6e+s+N6W0pSLXKspycn/s0JUM6z4DW/B+5i2eG7GLp1BymsWj9MkGUf4h7ei0eQs+zbmDoxDN+WbN5no/JKQ+bwQm0LE/ZzoOrOfCXbsKCJLZaoECgYANy8HoNpLns4oVUqr5trHRsNHxJ1VNRW4C/ovI/GAUZJgTQVFRy1GhhvcffwgBuob89GcwnnUKsVS7JpeydUm9ZMXpCZNLTGHevGqhYwD/Y0BTDwUZZyYOcuQXjL1yaHlicW8678ThE5xXlF8kzBFMkc+bAaaLefLER3/ehwyywg==
2eb236af-fc7c-40a6-b6c3-ddad60a50a00	95e4f666-d3d8-48c0-874a-dbab75d5ead8	priority	100
f0fc1807-1689-408a-8ed9-eb0c1d163e59	95e4f666-d3d8-48c0-874a-dbab75d5ead8	kid	3aacd666-ed98-4a65-84d3-dce1ce6c7d37
5cd72240-dd96-497f-af07-6af48903d305	95e4f666-d3d8-48c0-874a-dbab75d5ead8	secret	tzFVkZSeOrggVagUntFQFA
268d84ce-81e4-43dd-95a9-f8096a711cab	e2440177-15be-4bb2-9e6e-07a479420650	secret	F2kjPd1JsNv0zNOtwicTJ4xmFrZlHh21s0kMHE3PbqTtn_CWawVgxch9-Ai1ht_Uc8kn9cdvazszHNYbqVqkydpM1ExN-Xfkg1GXyXg-EjrAmbgVRcEqZfxkCrcFong_DzK6qktO3ktJA8QwSyabX_O6HvUwRzg68Z7yqAarWHE
777dffd2-9971-4701-a1b3-7f671e7a2b9f	e2440177-15be-4bb2-9e6e-07a479420650	algorithm	HS512
a9d27139-c2af-419a-acce-ea009c56a7af	e2440177-15be-4bb2-9e6e-07a479420650	priority	100
3cffa129-df3a-45cd-ab4a-c5c561e5f5f8	e2440177-15be-4bb2-9e6e-07a479420650	kid	ad944b82-0c82-462b-8ec4-cf8d0ece99d2
1a0587a4-e383-40e2-a27e-20be0c784483	0dc316c4-7be2-46cf-80c1-400b1142c142	kc.user.profile.config	{"attributes":[{"name":"username","displayName":"${username}","validations":{"length":{"min":3,"max":255},"username-prohibited-characters":{},"up-username-not-idn-homograph":{}},"permissions":{"view":["admin","user"],"edit":["admin","user"]},"multivalued":false},{"name":"email","displayName":"${email}","validations":{"email":{},"length":{"max":255}},"permissions":{"view":["admin","user"],"edit":["admin","user"]},"multivalued":false},{"name":"firstName","displayName":"${firstName}","validations":{"length":{"max":255},"person-name-prohibited-characters":{}},"permissions":{"view":["admin","user"],"edit":["admin","user"]},"multivalued":false},{"name":"lastName","displayName":"${lastName}","validations":{"length":{"max":255},"person-name-prohibited-characters":{}},"permissions":{"view":["admin","user"],"edit":["admin","user"]},"multivalued":false}],"groups":[{"name":"user-metadata","displayHeader":"User metadata","displayDescription":"Attributes, which refer to user metadata"}]}
554d3f35-2668-470b-a342-15f315dbef6b	1720d20f-23a0-4d19-b1a7-e408ae161b34	priority	100
c21a183e-a7c2-451c-82d4-227cebbc98a5	1720d20f-23a0-4d19-b1a7-e408ae161b34	privateKey	MIIEowIBAAKCAQEAjNSr68p/G6scgaKku+MQxLQZI6J/Ov9i9Fx9gRsJvKXPWhPWvgDReWma3yg7M0kxvcDU68dV4aVGZO1xJmg/hlLIg8BpNoAtUe5cXyzGE9QcKu/bjkDERF2cq/eAu/95F0fki2ilT2I5JiRGBo9V5r3x9/JJMm0MInXNvxoq8whrqIAwBZdkGHeq3hI53YEOTUpf9en7lQBHH36yMVfG4Xk3/JUsS1ckrikq5k6IZ4r7OLKv0wJ9TVdtQR/Si6cTw4LLMxTstgJKSdXxjoc0ZhEscuNSB5CfebJrM34Gj8pWd67pDGauUS6KFaVcTDTUzrsq8FSuhe6amNd+JWn6rwIDAQABAoIBADfc+q9nHWGP0Bh6OEdRbGril+BDSp3QBWQyNhSa8ZNT4Hr2SKYI9A7pvaXMsyMGY0VGcw9t/FqsMU7CwzH9g0lYmDJvBi04zgFkgF6+h3oBFwVPLPPyLAiEa6vpWzb3wYRjH7zPD1f8effvxpk+jVAgw5Vblf57NCeNPEaUbjoF4+nXdepMbLyjiX1KOKtXV8pdbuz2sWQttfFdxtiqzGneAzIVBaLvF573g1uEdPsYuys6Z5k5SlkUfCxEOvvDHBnhll1on3t3IKpcUgKDtcgf5q8UY4I0CylPNgNTFNS7MQfF6tW6GQEPXlWt8ow4+R8AcDYk1NfdhGAm6GTBdRkCgYEAwSI1m/BH0AHSG8S0cRdDwslscVLa8NBSGXgt7qh15l9ANHIA2nr2o++Fhq66jE1IGHLu1zscwQIGpR/Tgm7BAFoWpAL5df5UY5985GKFIYcH79BAfb7i/CaIvQ9/82tty+p5tupdzhIKX2jeBi8AKvy9OP2ep4+hdk1isPBSlfcCgYEAuqwSifFVrHhe0sIFpRJcPos+0tapznVqwaGCG4C2YT+Bu1+GKCFJWdd1XrGPhNqf8SAow8ZGc6uZ1nSnLZe17Yxfzo0A68JDpn6TcX/pUHG46vNdbuSyQLu8BTx8tjpdjs+cICPi/EpsPc7fblFIrg4Q4TTheXJs3jQid2PRswkCgYEAqnT4/8KYfxu8R0nbQB0abya7kWFhXz1d2KDbWVJRjJvw3Njpq+rvGE1kejRo7T+gLAP0jP3dKPQSzVZDpVD/AsKATQ1bAysPbEXtQt05RxgYhy40XUdGqumPsd2mPj9IzrsJ5ckANcpyYTb7DlYZPdeHYm9lwdng1bsDKctR+I0CgYAdYACW1nRd7J83WTLcNBRx/yWGtiMIiy+egtTfkRSiHwVCQBjzbbGGQsKEgTqNdH3gyue/Tw89Go7d0YORSCNn20QkU8oGT46nv5liLffAIfUwe9WDItfuGdzPkiIp5utcEs2FvT/15Zw86bX9PStLwIjld5XXr6r0GI4n7XxNSQKBgBAyBOZaByiMSTO59ArtD97RW6vwoPhN4uRdfs1JcRoPJgYsYWJBxBsKS1q7daag/lYqdUPalCR7hZ9b6a75RZLszL3WvbluCJ3bRSz1KvOUOXHqnyG/IGfoXHjUf2wj1XyLdoqeu9nA2bBYlnRbUCjjnzczrAa2hgfjPJxRZS7A
bcfd6126-aa91-4c30-ad79-6b68bb650c56	1720d20f-23a0-4d19-b1a7-e408ae161b34	certificate	MIICmzCCAYMCBgGd3tZQrzANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZtYXN0ZXIwHhcNMjYwNDMwMTQzOTQwWhcNMzYwNDMwMTQ0MTIwWjARMQ8wDQYDVQQDDAZtYXN0ZXIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCM1Kvryn8bqxyBoqS74xDEtBkjon86/2L0XH2BGwm8pc9aE9a+ANF5aZrfKDszSTG9wNTrx1XhpUZk7XEmaD+GUsiDwGk2gC1R7lxfLMYT1Bwq79uOQMREXZyr94C7/3kXR+SLaKVPYjkmJEYGj1XmvfH38kkybQwidc2/GirzCGuogDAFl2QYd6reEjndgQ5NSl/16fuVAEcffrIxV8bheTf8lSxLVySuKSrmTohnivs4sq/TAn1NV21BH9KLpxPDgsszFOy2AkpJ1fGOhzRmESxy41IHkJ95smszfgaPylZ3rukMZq5RLooVpVxMNNTOuyrwVK6F7pqY134lafqvAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAIfePNCSaRrYM8CSaFMBsLwl/7/vzyVoYHr1JhKkcRqDcoPbFKtx2Z/mBiRYBWbJ6k9Ak6RRU/vT84vcf+HyzzK2LDWLfHlVs5VCuHET72cjW2N9h+9eRWznC3Yvv4wMjzfPWSiQYNqtIri0W2fbF5oARUQdFpyF2/Ooyh1oz/sOsnmh3Xl++5WoAfxYm5HCBSQO5kJRBEDdZ1Xp5EI6Z8QC7MpLbmWeVdlQwl2pC/QcFKZuf5e96LxQ2f6o31jp07ItKxX5SUWApuX74twNE3IXU1ZJwIzg2HiEbGGa0jr2YUql6G1BRXCmMkXF94v61VnRHH7w2OJgztzwbXzJ3c0=
3a8f33ba-a866-48ee-aa8e-3125267c97ad	1720d20f-23a0-4d19-b1a7-e408ae161b34	algorithm	RSA-OAEP
b4dca8f4-ff78-4e72-a42e-459eb7e09d6d	1720d20f-23a0-4d19-b1a7-e408ae161b34	keyUse	ENC
b5e31866-ecf3-4d78-9678-724d2e64600a	0435310e-2b98-4960-9aec-a8425901ee1e	allow-default-scopes	true
4962da0d-653c-45ba-94d8-c07ba6de099e	2497eb6c-8552-49e6-a159-493bac003a54	allowed-protocol-mapper-types	oidc-usermodel-attribute-mapper
54d5a7c5-c11c-496b-9264-12813601ab86	2497eb6c-8552-49e6-a159-493bac003a54	allowed-protocol-mapper-types	saml-user-property-mapper
98fd3d7d-3a63-4932-bcf2-273878f638c8	2497eb6c-8552-49e6-a159-493bac003a54	allowed-protocol-mapper-types	oidc-full-name-mapper
0632e42b-ce5b-49a8-abcf-2c9bb5250f49	2497eb6c-8552-49e6-a159-493bac003a54	allowed-protocol-mapper-types	oidc-sha256-pairwise-sub-mapper
ae4db3b2-6335-42ca-a4b6-424fbedca121	2497eb6c-8552-49e6-a159-493bac003a54	allowed-protocol-mapper-types	saml-user-attribute-mapper
c6883b0f-5ae5-40d2-a6ec-d6e4d5b9791f	2497eb6c-8552-49e6-a159-493bac003a54	allowed-protocol-mapper-types	oidc-address-mapper
9757fb9b-6078-4830-bac7-f1471d621dd5	2497eb6c-8552-49e6-a159-493bac003a54	allowed-protocol-mapper-types	saml-role-list-mapper
81a983bf-2e27-4a4b-95b5-931a17e659ff	2497eb6c-8552-49e6-a159-493bac003a54	allowed-protocol-mapper-types	oidc-usermodel-property-mapper
ad2ed6ac-1f12-4a2f-a8c6-165ef4134bd7	a8a74107-2a1b-4d5b-a0a9-7de26c27b421	max-clients	200
a5846b74-8e10-4cd6-9b31-ffcc1164b6cc	06fb3851-85c9-489e-81e0-37830c3bf2a2	certificate	MIICmzCCAYMCBgGd3tZS6TANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZjc2ZlZXIwHhcNMjYwNDMwMTQzOTQxWhcNMzYwNDMwMTQ0MTIxWjARMQ8wDQYDVQQDDAZjc2ZlZXIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQC0WoxsZFPk0LR6Wgk2XUxlKCNR/DiDRVfGB796g6PsFcnu5NgLYSClWNrYnW4tQDDFNenlftU8HKb6AqTiwokD41s9Z/8UoX60kIO4/eC23SbaO/ab5cjqbHhBr+eL5r8raMVZ6EDYDolC8VKVF3OPzXzaqsy3MZb29Si9hanMzUBAVZsaGXWxlq2b4GyyIVhx+kM3x18wHO1IPSGwhp+OQADzcCPjmsSTMmNztVRVROQQCGW1A6Z9y7OnEw6YtNRqNohApuO3dxtYix+hhMozL/RKkQ0/jVY6/Mu2wvfqUhS3pq5wMn+UYKgWbuXg74NXqoIIGTnr94jPfUeqDI/nAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAAggJMRm7JaFFbdOL/nbfpVO5kF0VHJJ62XQd3e1zfBKxdzTZvEUMj0+q0K7Lwq0RYf0y256QjDyw98cCXLsDOrlRi7lKxaYK6iaSVNjx4uACiB/xASxSuCXlFYGvT77q8jwWuD90bg8AoF5aj+YS3+oClG4q1F+P18nqRYOvKmWtx5vkzRgBJGHsn6BtBDEaAFHl0f4i/2ceJBwlD2X6fCT9x7YE7vqPt73/llv1pPLzNqO40TxG0UmXZ+x5VjTFyOtzJkB4qMOUDA8r2ZQ+AVHgYgHyK8oERzwxbJWs5CwRR5bZrvJrCuvvJAcTZ7FNfTeTqoFQzdfOoHaEpxiFi8=
cb8683c9-a96d-45d2-b0f4-688d68db115b	06fb3851-85c9-489e-81e0-37830c3bf2a2	privateKey	MIIEowIBAAKCAQEAtFqMbGRT5NC0eloJNl1MZSgjUfw4g0VXxge/eoOj7BXJ7uTYC2EgpVja2J1uLUAwxTXp5X7VPBym+gKk4sKJA+NbPWf/FKF+tJCDuP3gtt0m2jv2m+XI6mx4Qa/ni+a/K2jFWehA2A6JQvFSlRdzj8182qrMtzGW9vUovYWpzM1AQFWbGhl1sZatm+BssiFYcfpDN8dfMBztSD0hsIafjkAA83Aj45rEkzJjc7VUVUTkEAhltQOmfcuzpxMOmLTUajaIQKbjt3cbWIsfoYTKMy/0SpENP41WOvzLtsL36lIUt6aucDJ/lGCoFm7l4O+DV6qCCBk56/eIz31HqgyP5wIDAQABAoIBAAe4gJ5tDDJci/1Y4ycvFRHs3GY4ibHofAjG4s0fMKl9FjApdDqqQf9K9rUxcQHJIJR3zUWEQnifpAyC+cx8MpOaCLWo650A7b2pGhp5CSiK4jchdSFm8DB+PZUCS9/vVRZma84rD88hx0i4WqY9Dai+hpH/oA06RZG8ceaz/7H8B50J6J5Wu5qDzHPeIVQF+dWrdpL7WZNSs9Qy7BU3gnHIDzyTY6f0zKMjKOZ1RagGAUEeNklgXTosQqWBl4532/O3+Ap9JDwC9maVSkNIc4Sz544YA38+nDuu3XC4lEx9pmOEsKA+ugI1UoaCqSdcmWB0G0Wv5ewrphzvwdkcD1ECgYEA6LCNQ2S5A/jCXoKOpTomNqiQtGNHta+qacph3eQ+TefVhuNmQbXN0qEsf3s/ca+nUVhEA2jWoll+6HfWTztVsUAUs6079fwuIpZDclEcjHGxYx1dxCN2+cf5S75g+DxjzgUFJM4JP5vRCrR3jFmda7eVP4oEy0lVyM3TsIbQicUCgYEAxmvQV8RcJpUYNdLIWkg141hPJ64E+X6tmQZgGHPuZmr1KUfyVzz8uZSapA0RE6kSwqHBEoDwSqhUygzOGV6uoFV4x+GPQqDlg8z+inyBfo7VbnZMbRafe5vfm6qJZ94YBx+akcKp7SJfc0MJXcO1YiEStaU6z+DsCkoVk31gCbsCgYBCOy6aRisbZEz+1a6AfSKvYB+AGNoqbsvUvNRKclMBncF7WXKbtYHWOCYQSyZt14+KadNCHS8qmsqypJmNh9gGUbUSx3ZPt+3xzk94VHoJx7qz+YHc+DM/OZpN4ux6+8V0uJ0UMskTH+jKYT+95SwXovOKWGCw9DjEpUFh952X+QKBgHFJmTijKiH1Ok9wu2eglvPotbjoCHsSsrcOBsuvVUwwgS1CoMDiV0D18Zz8wOVCwS1TAVM5PvjBRzfdO8cMYhO0+TLWO99E0gYAgsw67gx+LKnW7SfTpNcEVhUgtzcQfROEHdJfHHoCCBFdEvnwBZ2zWGVRo1SRDPOK/OqqyKyFAoGBANVuolGvzmG65CpDae1qHfIbTwdXEPNaeDhN3W683y4zNGkUNDoSI46NYt//6a5vnA9dDVJVEVfR6AxVcWYvnX82K9r2Vju3lwiXhan0V7wl7dultcODIiOcqEZuj92cE768hFWrYHoEGHgBVfeF43Ao5IoAUEEimqOcnxNStKSm
88669f57-a690-4483-92a3-4337ce112dd1	06fb3851-85c9-489e-81e0-37830c3bf2a2	priority	100
a784b9ac-e031-488e-818f-f7125a4d7647	3bfb7310-7d80-4919-9970-f3be9b30ab4c	privateKey	MIIEowIBAAKCAQEAwmPIEaO9lAOVpw/oQXoFQmpi9UN1lN/+SayNjbT5Wjablg7mT7EihDhK4l6FF1xg/bxLpXaSe+9IFoy+WV7IQ63GPqvq5OFmUE7rv4+qKir4SGwNbjArtSUsHtXfABIO3BKYDBLKQhqTlCBGoXdr90UGGhsQLaQU2V+/wHU8fHBHSqS3WTKoJmxL+2SQjCrFU30N1BrorLc1xdFSUTrIUtinvOR1dKtpMTXmSRutUm9sUA0JoABds9k3UWAX1svMiplNX7YhT4zswiJCNjdHBzTk7BWS5BF2ZApv9t0kPHRNxbJ4Y2FCsHQUeGDn092p6lxX/y9FEP8PTGj1KtyQxwIDAQABAoIBADRfwQRrqwTpsFUKNqgJkcgytMXjLpd1gGRmPt9azsItK19TVV9MWQHpztdN4ysHo0RKCtGicFY/Apu8wP6ASJHfjKXPGSMgzbm+gcsjkJP67tlIb5fsF6KfSNNoCUTSGLnXsqqyF1eXJIMI7S7M58SADuRSvVmmt01X/GiEzc6y0lIoLEmGmnZulYtwvKt667k8nuqBrBSZvMcLHRtC+/a/OIT3wLyqY7rzlNwCpb70NCZjr9UTrXKYhs3zyuXUGoe5UTvUhEkPakSrmOQ1TPCdwYnWfUoxiYge/OA7rC3anDZOw9TCe8/C53De6MqJ4o3SP6LS6KazL754CPdkeMUCgYEA/+6VHYZno8ImImrEPKuXbbQhDFo1McxVGPL5BgqYHQuXqAR/wVCh1AgvEJnTKXT5h1tKX2LVhwU3h33BmFtU1rVCB/f0QQ926tAdv8m8ShsEtfbW4HWqI3q7f0nsh7maUr3A0cffQf/CkgmuO++vONwV/C6oFeqAA8l56qVkt8MCgYEAwnECwaHdEx8Jq1+L0YlJ2xMKui4SL5zVASSHWlr5lPKrXDrX3cQWVdIGwfkkx+VZJKUUztXlthu1VUsrQT1/9VmlOlsJ85jPtXd7UgZS+Jp3hrph3DoCkO6QSlI/E4hmalWELHmmdQTyJ07VU6ge2taMC1lf95tLk9tCYmF99q0CgYEA4vOq/9ekKC+OqY6MHlD7o6jMdau46EQOYmV0NstGQNt6zN/QepkKKIBpXAtMmcLFVCa8OQHn4CfcKiZ2eqji/tMVjwNuchNInMmY1+4JLp3u+3285qbxDS1U/3eKbIFGPIFQb7cSX/BxlhdHjpbphz6DsHGfVG/yvWj41/965QkCgYA08n0jqSYALPV/GxeByXa5FyhWpnEBUh2WoBHTgu5vpt0O0l8x3lGOsRByBZwEaumpVuKhqBFTU5w/S6bNryeG8hBSIbRGBxiYe56zKVGyrK1bnKlFRO6p9KyJ8HeIpB3vWrYRPlcbims+VPM2QpOUV9PuyzmcvUcJTi13iMC6SQKBgDVEzrQQncxnalNs6KkJM72Mdg4sVj1H8t8ThEOl8gy0tfBYzUoFVoFllNnDenVSxrwf2XurOhHzvFxqDPz6v2FTbMdL0qBvtL8iE/nNOIKJfF9lJkwdizZNhpk3Xdu6esBDFe+6TKnYYFNuvfRLonLLYHmxHElDKz0JYBlKm6mP
45717cae-4b84-4fcf-853f-97125086aab3	3bfb7310-7d80-4919-9970-f3be9b30ab4c	priority	100
12960f79-d3d7-408c-9b1e-d15d97206d49	3bfb7310-7d80-4919-9970-f3be9b30ab4c	algorithm	RSA-OAEP
640e9323-273e-43e8-aa9c-bfd61fcae5c4	3bfb7310-7d80-4919-9970-f3be9b30ab4c	certificate	MIICmzCCAYMCBgGd3tZTSDANBgkqhkiG9w0BAQsFADARMQ8wDQYDVQQDDAZjc2ZlZXIwHhcNMjYwNDMwMTQzOTQxWhcNMzYwNDMwMTQ0MTIxWjARMQ8wDQYDVQQDDAZjc2ZlZXIwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDCY8gRo72UA5WnD+hBegVCamL1Q3WU3/5JrI2NtPlaNpuWDuZPsSKEOEriXoUXXGD9vEuldpJ770gWjL5ZXshDrcY+q+rk4WZQTuu/j6oqKvhIbA1uMCu1JSwe1d8AEg7cEpgMEspCGpOUIEahd2v3RQYaGxAtpBTZX7/AdTx8cEdKpLdZMqgmbEv7ZJCMKsVTfQ3UGuistzXF0VJROshS2Ke85HV0q2kxNeZJG61Sb2xQDQmgAF2z2TdRYBfWy8yKmU1ftiFPjOzCIkI2N0cHNOTsFZLkEXZkCm/23SQ8dE3FsnhjYUKwdBR4YOfT3anqXFf/L0UQ/w9MaPUq3JDHAgMBAAEwDQYJKoZIhvcNAQELBQADggEBAK7K0uzGk4VLmFZI804UvqjHX5I7SSXgQDjpVvbB0ZNOFQkp8jWYUXeCfCRu1vaVi3JVgeLy6zFvryfId/0XhL5ihMwU4dTJ6tQHB3Buu6EVTIAk87q1s6JPK3gZseTvB0O9HAo/hhuYBd/IDIwCnkkrJ3cGPt3M4w3U+ung7B8sTeU7Q7iZiaPm4mdy6ep9DdzdtvaRuGjX/h0P4nZCt/68rMJ8oaJHTZpES5pROCLXYNgGn6gpopfIkNWCjKQWV1PgvsC344Do1cF7P6XqmUBOYCM/dS/iJjx7PCyTvmi38v9lRMTF0IQ7tictqee53ZHgrMBq7bHAWp4lrW1E5GM=
b9b5d99e-c973-4072-bda8-eaa23ec3dd36	1be1f438-1208-45fa-bac7-44ddba7abeb3	allowed-protocol-mapper-types	oidc-address-mapper
b57f4f72-ed36-45b1-b509-47693f057568	1be1f438-1208-45fa-bac7-44ddba7abeb3	allowed-protocol-mapper-types	saml-user-property-mapper
31ac5613-3aae-4aec-8769-d9c0b25dcf92	1be1f438-1208-45fa-bac7-44ddba7abeb3	allowed-protocol-mapper-types	oidc-usermodel-attribute-mapper
f498aeeb-d13e-4afd-bb2e-f4e69e46a01a	1be1f438-1208-45fa-bac7-44ddba7abeb3	allowed-protocol-mapper-types	oidc-usermodel-property-mapper
04d95ad6-a74c-4322-ad44-57f45ce96bc2	1be1f438-1208-45fa-bac7-44ddba7abeb3	allowed-protocol-mapper-types	oidc-full-name-mapper
7c9f100d-2f58-409b-ac79-266deb3c71a9	1be1f438-1208-45fa-bac7-44ddba7abeb3	allowed-protocol-mapper-types	saml-role-list-mapper
a6f5203b-f057-4b0b-8a68-e0e86263af0b	1be1f438-1208-45fa-bac7-44ddba7abeb3	allowed-protocol-mapper-types	oidc-sha256-pairwise-sub-mapper
fd024b94-a966-4f35-93bc-4c4b4e35f54b	1be1f438-1208-45fa-bac7-44ddba7abeb3	allowed-protocol-mapper-types	saml-user-attribute-mapper
ef057dc2-14e8-4b24-b082-0d143bcd07fc	42739c0e-d602-4f60-a82e-dee3b9234805	priority	100
616eb3ab-7a47-47a0-8c8c-8e79c2faa7ae	42739c0e-d602-4f60-a82e-dee3b9234805	algorithm	HS512
536263f0-ccbb-4743-9044-22fc0cdc6ba0	42739c0e-d602-4f60-a82e-dee3b9234805	kid	2075932d-5b18-421e-97d9-47b18eb3aa89
4b8fef66-3430-44c2-8ddc-fda05c4d859a	42739c0e-d602-4f60-a82e-dee3b9234805	secret	VnUWS6GU1-nnysUxHrU9IP6h1_feN5oz7ajqgDK8Aw-tn_nnjaCf0WqthUfbPAce1Xbi3ZQ_IatIUW-4_BThPRaS_u6aOaXBIx_NR_MGD8JSs0KDIrf7KaXhVYhFp0yYHAtEvRdntTMiOIffgP5w5F8VLUVPB0H_8IeFJrwvU7c
b6b6e849-4f67-4d4a-a901-6d5b000dd57c	dd78c320-42a6-4334-a82b-c74a8a72671a	client-uris-must-match	true
30837a40-4af2-40f5-a4d2-e8d87a96109d	dd78c320-42a6-4334-a82b-c74a8a72671a	host-sending-registration-request-must-match	true
938efa65-b8e1-446a-9628-f79876c4b92b	2baf6124-d931-4482-bb64-76ab445c7667	allow-default-scopes	true
eada7d8e-2df4-4e8a-bf14-fbc4385f16c2	9b4c06b1-2135-42c9-add1-43122569209b	secret	rEOoKX0fy6317uFWlATWBw
33a2b4cd-beb4-44ed-936d-3348b521178a	9b4c06b1-2135-42c9-add1-43122569209b	kid	053ca5f7-712d-4df5-9f36-900261f86a9d
7a71aada-c650-4e54-8aa8-85f1bd100318	9b4c06b1-2135-42c9-add1-43122569209b	priority	100
\.


--
-- Data for Name: composite_role; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.composite_role (composite, child_role) FROM stdin;
36c982d0-3c1d-4472-95f5-63f2f2554ee6	394521e0-fc27-4a81-b07b-3f2a5808a5cd
36c982d0-3c1d-4472-95f5-63f2f2554ee6	3ca274e2-91d5-4cbc-82fe-c92630376a1f
36c982d0-3c1d-4472-95f5-63f2f2554ee6	58858844-d6fa-4904-8ec8-ef3ddc817110
36c982d0-3c1d-4472-95f5-63f2f2554ee6	c5b9c122-60d0-4b81-8cbd-ebd68bf8bece
36c982d0-3c1d-4472-95f5-63f2f2554ee6	2a9eba64-cdd8-44aa-8bb4-3f372816a70b
36c982d0-3c1d-4472-95f5-63f2f2554ee6	8476b2b7-1806-41c9-8b2c-70f957866126
36c982d0-3c1d-4472-95f5-63f2f2554ee6	aa4626bb-7346-44cf-90e8-44d8ca5a2772
36c982d0-3c1d-4472-95f5-63f2f2554ee6	ddb10a95-e481-43eb-bcf5-23356332f21c
36c982d0-3c1d-4472-95f5-63f2f2554ee6	27be0898-95e0-4fed-9940-3724e1341040
36c982d0-3c1d-4472-95f5-63f2f2554ee6	cf0edf92-25a5-402f-9860-784f35447df0
36c982d0-3c1d-4472-95f5-63f2f2554ee6	17a019fe-a432-4319-b37c-ba2defd12b8d
36c982d0-3c1d-4472-95f5-63f2f2554ee6	3a1c7506-233c-4db5-871f-8a08e1d8513a
36c982d0-3c1d-4472-95f5-63f2f2554ee6	123a58a1-0ecd-42df-a7f8-ed74d8db0018
36c982d0-3c1d-4472-95f5-63f2f2554ee6	eceb69d0-611e-4c2f-a343-65ea0e86409d
36c982d0-3c1d-4472-95f5-63f2f2554ee6	fca1df51-7265-4d82-b1d6-5a89286333cc
36c982d0-3c1d-4472-95f5-63f2f2554ee6	8edba74f-7ecd-449d-ba1b-5a111d6a23bb
36c982d0-3c1d-4472-95f5-63f2f2554ee6	fa9bfdbf-65e4-4e16-b832-df366d709ce7
36c982d0-3c1d-4472-95f5-63f2f2554ee6	36824ed7-29e3-4317-aba7-2d2c2c00ae1e
2a9eba64-cdd8-44aa-8bb4-3f372816a70b	8edba74f-7ecd-449d-ba1b-5a111d6a23bb
33aa8679-f89d-47ee-8e63-d57d79270440	caaf1f68-c0dc-483e-97c0-3738c9f80e96
c5b9c122-60d0-4b81-8cbd-ebd68bf8bece	36824ed7-29e3-4317-aba7-2d2c2c00ae1e
c5b9c122-60d0-4b81-8cbd-ebd68bf8bece	fca1df51-7265-4d82-b1d6-5a89286333cc
33aa8679-f89d-47ee-8e63-d57d79270440	27737e8a-5ec2-4c3f-b929-725240133d56
27737e8a-5ec2-4c3f-b929-725240133d56	a36ba95a-8b4d-4fb6-b23f-aa7104a9bc11
78f5e097-8089-44c1-9803-c64ced351801	c3234aab-13b5-496e-b713-dd22c6d5b4f8
36c982d0-3c1d-4472-95f5-63f2f2554ee6	af154f0c-e12a-4781-9b7b-e64914231226
33aa8679-f89d-47ee-8e63-d57d79270440	c5c2e4d7-4e88-4aa8-981c-4984a37ec40b
33aa8679-f89d-47ee-8e63-d57d79270440	9811a0e5-94b6-44f0-a1aa-11194fa0a1d2
36c982d0-3c1d-4472-95f5-63f2f2554ee6	bbfabec0-6afa-4ec8-8bcf-7eed2a200d02
36c982d0-3c1d-4472-95f5-63f2f2554ee6	471a5e1a-d25f-48dc-93b5-9f3dd6042930
36c982d0-3c1d-4472-95f5-63f2f2554ee6	ac625149-41cf-44a7-a4bc-09c81ed588ff
36c982d0-3c1d-4472-95f5-63f2f2554ee6	6e3b3ebf-20b8-4efe-88c6-be13a5f5d262
36c982d0-3c1d-4472-95f5-63f2f2554ee6	095c923a-1055-4e1f-8b23-936fd7caa3ff
36c982d0-3c1d-4472-95f5-63f2f2554ee6	b6d208f9-790f-4d10-9c12-3d3eb9c444c7
36c982d0-3c1d-4472-95f5-63f2f2554ee6	6c41cc69-db9d-49b3-80ab-6739d6ef06f2
36c982d0-3c1d-4472-95f5-63f2f2554ee6	17a1ebfd-6234-46b1-bab8-9314c7c51a43
36c982d0-3c1d-4472-95f5-63f2f2554ee6	8892692e-fdbc-4f52-991f-e6ca815ec4fa
36c982d0-3c1d-4472-95f5-63f2f2554ee6	778554df-db55-4ff0-ad3f-97ae274f0f96
36c982d0-3c1d-4472-95f5-63f2f2554ee6	dc8f3e18-5aa3-406c-8ab2-2395b608de1c
36c982d0-3c1d-4472-95f5-63f2f2554ee6	c9f1e0e0-1d39-48bf-9e41-78e01c5b7e03
36c982d0-3c1d-4472-95f5-63f2f2554ee6	46b2f33a-b7ee-4021-922e-b7c2da4da216
36c982d0-3c1d-4472-95f5-63f2f2554ee6	3d19a544-2c7b-4ce9-8f0b-061d66a3afc8
36c982d0-3c1d-4472-95f5-63f2f2554ee6	62871172-bca6-4bd9-bf2c-1a07a4f9fcae
36c982d0-3c1d-4472-95f5-63f2f2554ee6	e4de23f9-d355-400f-89ce-bd1d2d75236b
36c982d0-3c1d-4472-95f5-63f2f2554ee6	e691f5aa-11ef-4230-b6d5-4d5b25abdd5e
6e3b3ebf-20b8-4efe-88c6-be13a5f5d262	62871172-bca6-4bd9-bf2c-1a07a4f9fcae
ac625149-41cf-44a7-a4bc-09c81ed588ff	3d19a544-2c7b-4ce9-8f0b-061d66a3afc8
ac625149-41cf-44a7-a4bc-09c81ed588ff	e691f5aa-11ef-4230-b6d5-4d5b25abdd5e
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	bd2e3de6-6bc2-4f17-880b-9be4367ed89d
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	f3f65afa-a38b-450e-a812-6e1f0b6b5f58
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	0e78d5e6-550e-445f-bc61-21409b052e41
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	ca35c48c-f30a-4c0a-89c7-adab1347c185
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	cf817ac6-42b0-4494-9df0-3c6a9bbd2de7
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	ee1d0b58-e578-4b1f-b189-5da60ed85f15
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	e6ff11d6-a1c1-4c1b-8818-47c07f24d7dc
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	de7e7a89-0e7d-4bea-aed5-93f32f824640
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	01d5015d-222d-4445-906b-971bbe4df9c8
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	81ba14ed-6f2c-4e24-abb1-ef97b6c87057
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	92bd35f9-b02c-4ae0-b18f-f3f78c08d1f7
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	24e9d6a5-f1a4-481e-b855-1cf6b92027b4
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	826dabc6-e7fc-410f-bba4-90a29f234ba8
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	962f06a2-f97a-4c53-9793-be7f45360ed2
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	b7cf881a-f662-4c05-90b9-8cce965cc72c
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	6294e231-a2c7-40e6-95e6-bf7cce8b5570
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	36b77f6f-bc11-4f40-9922-7ef323ec2691
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	01a0f4a4-a6d1-4dce-afdf-fe14f65dcf65
0e78d5e6-550e-445f-bc61-21409b052e41	e6ff11d6-a1c1-4c1b-8818-47c07f24d7dc
0e78d5e6-550e-445f-bc61-21409b052e41	36b77f6f-bc11-4f40-9922-7ef323ec2691
1dec6fcb-0eec-473f-8a1c-e3c12ebcd73e	bc8c26cd-60af-42bd-956d-b52022a8159a
826dabc6-e7fc-410f-bba4-90a29f234ba8	962f06a2-f97a-4c53-9793-be7f45360ed2
890da050-44a1-4d3a-aa8a-3c6ad9d225d9	9c7d0834-aa6a-45db-9524-65370194d514
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	1dec6fcb-0eec-473f-8a1c-e3c12ebcd73e
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	abd702be-194e-420f-9a46-821e6340a8dd
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	ffc312c1-b2ef-49e3-97bd-3b56b6102ded
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	fc77baf5-cf87-49ff-9915-7583c284d482
36c982d0-3c1d-4472-95f5-63f2f2554ee6	0aef58e9-e808-4809-a53d-d1ae5c8331ec
\.


--
-- Data for Name: credential; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.credential (id, salt, type, user_id, created_date, user_label, secret_data, credential_data, priority, version) FROM stdin;
247cda42-9704-4f28-834c-c6e6be93cce0	\N	password	dad2c622-f878-4d62-8ae2-39bfe52003ae	1777560081396	\N	{"value":"O1lNGOdRSWSFNgFYZEZLh0WD1/77y4S40KxHWK6oigw=","salt":"qRItDmze4HEUyjhlRfukeQ==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
fcc2052a-e2db-493a-84d9-ab4142ca1b72	\N	password	392ff97d-168a-4526-af46-bc10528b7962	1777560084226	\N	{"value":"h12SVUTKJuf0hjfrH8f7gLCP4aMJOv6Mxci3n+rhDCU=","salt":"wh9RdLaxz4gTjV1gXLBlxQ==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
bbc9c010-3be8-4687-8230-50cc59b7e3a1	\N	password	8a4d8b38-9999-49c9-bcbe-c30bb730b53c	1777560085908	\N	{"value":"/N+MRwnxnKQMJqbkjiE6bOKnEgr4AwN3zBJ0BgP1MtY=","salt":"dAWVCz6fnYaRWUSwqT+E2A==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
9bc8409c-9238-46bb-8d4e-ccf98019b964	\N	password	602688a7-1050-4a44-8633-cb58f2b0625a	1777560087615	\N	{"value":"EDIoWaTSqhDIHW3Jz6Jm3AkEKYDMbmHEQoA0gRJQ1+Q=","salt":"Ky5seSu7LWOxH3xYvI8QEQ==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
86c595c4-917d-4f23-84d6-4b9dd65aed36	\N	password	d2f94b3d-be17-4a59-aa5a-8373bc7aea4c	1777560089325	\N	{"value":"0yvaQ9brWqR7PijkBDVRrYOoXnU71fKmXz8L71ixn2c=","salt":"1Y6lfvFiLtUOJxl9hKA5tw==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
33c06630-4dc9-44b1-9e46-d4767820f630	\N	password	3ef46cae-90b7-4930-a8fb-43e6e19c0aa7	1777560091006	\N	{"value":"8qSif3Ds0Jn2F3z+9OSpBTczykZPVuyieCzXy9hdiD8=","salt":"CeIcTV+QdEBzr3YOrIAWvQ==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
b21b6cc1-d28d-4c45-b508-b932992da194	\N	password	1f2bad2b-bc71-4e74-abbd-31702831125e	1777560092614	\N	{"value":"VhQRzp65p96Nqm8PgQHydTSlLsJ7V2LzOi0QbV6cmVg=","salt":"s/S57YvnEGJck99U1mY9wA==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
d5c03788-1977-43ab-ab49-4c95c4b84652	\N	password	18e39e37-b032-4221-b99a-852900598c3d	1777560094359	\N	{"value":"pS+emCOFbOCyyEk1xaLpkZbvG2sP7k10/D78ycB+LJY=","salt":"tiuUMAh1m7Zw7WbLynew+A==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
c3279e78-1525-4d1e-b2a7-e98dab74b5d3	\N	password	9dd77269-24e5-4698-b16e-3a8b4ad7500a	1777560095988	\N	{"value":"3+lEClpdolTYEYoERXilHCxPKm86rBlXHvW46wqWY9o=","salt":"8NSkt73C1XRmNvakRjeRNA==","additionalParameters":{}}	{"hashIterations":5,"algorithm":"argon2","additionalParameters":{"hashLength":["32"],"memory":["7168"],"type":["id"],"version":["1.3"],"parallelism":["1"]}}	10	0
\.


--
-- Data for Name: databasechangelog; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.databasechangelog (id, author, filename, dateexecuted, orderexecuted, exectype, md5sum, description, comments, tag, liquibase, contexts, labels, deployment_id) FROM stdin;
1.0.0.Final-KEYCLOAK-5461	sthorger@redhat.com	META-INF/jpa-changelog-1.0.0.Final.xml	2026-04-30 14:41:15.954229	1	EXECUTED	9:6f1016664e21e16d26517a4418f5e3df	createTable tableName=APPLICATION_DEFAULT_ROLES; createTable tableName=CLIENT; createTable tableName=CLIENT_SESSION; createTable tableName=CLIENT_SESSION_ROLE; createTable tableName=COMPOSITE_ROLE; createTable tableName=CREDENTIAL; createTable tab...		\N	4.33.0	\N	\N	7560073650
1.0.0.Final-KEYCLOAK-5461	sthorger@redhat.com	META-INF/db2-jpa-changelog-1.0.0.Final.xml	2026-04-30 14:41:15.961572	2	MARK_RAN	9:828775b1596a07d1200ba1d49e5e3941	createTable tableName=APPLICATION_DEFAULT_ROLES; createTable tableName=CLIENT; createTable tableName=CLIENT_SESSION; createTable tableName=CLIENT_SESSION_ROLE; createTable tableName=COMPOSITE_ROLE; createTable tableName=CREDENTIAL; createTable tab...		\N	4.33.0	\N	\N	7560073650
1.1.0.Beta1	sthorger@redhat.com	META-INF/jpa-changelog-1.1.0.Beta1.xml	2026-04-30 14:41:15.976829	3	EXECUTED	9:5f090e44a7d595883c1fb61f4b41fd38	delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION; createTable tableName=CLIENT_ATTRIBUTES; createTable tableName=CLIENT_SESSION_NOTE; createTable tableName=APP_NODE_REGISTRATIONS; addColumn table...		\N	4.33.0	\N	\N	7560073650
1.1.0.Final	sthorger@redhat.com	META-INF/jpa-changelog-1.1.0.Final.xml	2026-04-30 14:41:15.978586	4	EXECUTED	9:c07e577387a3d2c04d1adc9aaad8730e	renameColumn newColumnName=EVENT_TIME, oldColumnName=TIME, tableName=EVENT_ENTITY		\N	4.33.0	\N	\N	7560073650
1.2.0.Beta1	psilva@redhat.com	META-INF/jpa-changelog-1.2.0.Beta1.xml	2026-04-30 14:41:16.013275	5	EXECUTED	9:b68ce996c655922dbcd2fe6b6ae72686	delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION; createTable tableName=PROTOCOL_MAPPER; createTable tableName=PROTOCOL_MAPPER_CONFIG; createTable tableName=...		\N	4.33.0	\N	\N	7560073650
1.2.0.Beta1	psilva@redhat.com	META-INF/db2-jpa-changelog-1.2.0.Beta1.xml	2026-04-30 14:41:16.015862	6	MARK_RAN	9:543b5c9989f024fe35c6f6c5a97de88e	delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION; createTable tableName=PROTOCOL_MAPPER; createTable tableName=PROTOCOL_MAPPER_CONFIG; createTable tableName=...		\N	4.33.0	\N	\N	7560073650
1.2.0.RC1	bburke@redhat.com	META-INF/jpa-changelog-1.2.0.CR1.xml	2026-04-30 14:41:16.042779	7	EXECUTED	9:765afebbe21cf5bbca048e632df38336	delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete tableName=USER_SESSION; createTable tableName=MIGRATION_MODEL; createTable tableName=IDENTITY_P...		\N	4.33.0	\N	\N	7560073650
1.2.0.RC1	bburke@redhat.com	META-INF/db2-jpa-changelog-1.2.0.CR1.xml	2026-04-30 14:41:16.045067	8	MARK_RAN	9:db4a145ba11a6fdaefb397f6dbf829a1	delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete tableName=USER_SESSION; createTable tableName=MIGRATION_MODEL; createTable tableName=IDENTITY_P...		\N	4.33.0	\N	\N	7560073650
1.2.0.Final	keycloak	META-INF/jpa-changelog-1.2.0.Final.xml	2026-04-30 14:41:16.047493	9	EXECUTED	9:9d05c7be10cdb873f8bcb41bc3a8ab23	update tableName=CLIENT; update tableName=CLIENT; update tableName=CLIENT		\N	4.33.0	\N	\N	7560073650
1.3.0	bburke@redhat.com	META-INF/jpa-changelog-1.3.0.xml	2026-04-30 14:41:16.076642	10	EXECUTED	9:18593702353128d53111f9b1ff0b82b8	delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_PROT_MAPPER; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete tableName=USER_SESSION; createTable tableName=ADMI...		\N	4.33.0	\N	\N	7560073650
1.4.0	bburke@redhat.com	META-INF/jpa-changelog-1.4.0.xml	2026-04-30 14:41:16.093849	11	EXECUTED	9:6122efe5f090e41a85c0f1c9e52cbb62	delete tableName=CLIENT_SESSION_AUTH_STATUS; delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_PROT_MAPPER; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete table...		\N	4.33.0	\N	\N	7560073650
1.4.0	bburke@redhat.com	META-INF/db2-jpa-changelog-1.4.0.xml	2026-04-30 14:41:16.095459	12	MARK_RAN	9:e1ff28bf7568451453f844c5d54bb0b5	delete tableName=CLIENT_SESSION_AUTH_STATUS; delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_PROT_MAPPER; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete table...		\N	4.33.0	\N	\N	7560073650
1.5.0	bburke@redhat.com	META-INF/jpa-changelog-1.5.0.xml	2026-04-30 14:41:16.103497	13	EXECUTED	9:7af32cd8957fbc069f796b61217483fd	delete tableName=CLIENT_SESSION_AUTH_STATUS; delete tableName=CLIENT_SESSION_ROLE; delete tableName=CLIENT_SESSION_PROT_MAPPER; delete tableName=CLIENT_SESSION_NOTE; delete tableName=CLIENT_SESSION; delete tableName=USER_SESSION_NOTE; delete table...		\N	4.33.0	\N	\N	7560073650
1.6.1_from15	mposolda@redhat.com	META-INF/jpa-changelog-1.6.1.xml	2026-04-30 14:41:16.114492	14	EXECUTED	9:6005e15e84714cd83226bf7879f54190	addColumn tableName=REALM; addColumn tableName=KEYCLOAK_ROLE; addColumn tableName=CLIENT; createTable tableName=OFFLINE_USER_SESSION; createTable tableName=OFFLINE_CLIENT_SESSION; addPrimaryKey constraintName=CONSTRAINT_OFFL_US_SES_PK2, tableName=...		\N	4.33.0	\N	\N	7560073650
1.6.1_from16-pre	mposolda@redhat.com	META-INF/jpa-changelog-1.6.1.xml	2026-04-30 14:41:16.115718	15	MARK_RAN	9:bf656f5a2b055d07f314431cae76f06c	delete tableName=OFFLINE_CLIENT_SESSION; delete tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
1.6.1_from16	mposolda@redhat.com	META-INF/jpa-changelog-1.6.1.xml	2026-04-30 14:41:16.117509	16	MARK_RAN	9:f8dadc9284440469dcf71e25ca6ab99b	dropPrimaryKey constraintName=CONSTRAINT_OFFLINE_US_SES_PK, tableName=OFFLINE_USER_SESSION; dropPrimaryKey constraintName=CONSTRAINT_OFFLINE_CL_SES_PK, tableName=OFFLINE_CLIENT_SESSION; addColumn tableName=OFFLINE_USER_SESSION; update tableName=OF...		\N	4.33.0	\N	\N	7560073650
1.6.1	mposolda@redhat.com	META-INF/jpa-changelog-1.6.1.xml	2026-04-30 14:41:16.118905	17	EXECUTED	9:d41d8cd98f00b204e9800998ecf8427e	empty		\N	4.33.0	\N	\N	7560073650
1.7.0	bburke@redhat.com	META-INF/jpa-changelog-1.7.0.xml	2026-04-30 14:41:16.136268	18	EXECUTED	9:3368ff0be4c2855ee2dd9ca813b38d8e	createTable tableName=KEYCLOAK_GROUP; createTable tableName=GROUP_ROLE_MAPPING; createTable tableName=GROUP_ATTRIBUTE; createTable tableName=USER_GROUP_MEMBERSHIP; createTable tableName=REALM_DEFAULT_GROUPS; addColumn tableName=IDENTITY_PROVIDER; ...		\N	4.33.0	\N	\N	7560073650
1.8.0	mposolda@redhat.com	META-INF/jpa-changelog-1.8.0.xml	2026-04-30 14:41:16.151078	19	EXECUTED	9:8ac2fb5dd030b24c0570a763ed75ed20	addColumn tableName=IDENTITY_PROVIDER; createTable tableName=CLIENT_TEMPLATE; createTable tableName=CLIENT_TEMPLATE_ATTRIBUTES; createTable tableName=TEMPLATE_SCOPE_MAPPING; dropNotNullConstraint columnName=CLIENT_ID, tableName=PROTOCOL_MAPPER; ad...		\N	4.33.0	\N	\N	7560073650
1.8.0-2	keycloak	META-INF/jpa-changelog-1.8.0.xml	2026-04-30 14:41:16.15302	20	EXECUTED	9:f91ddca9b19743db60e3057679810e6c	dropDefaultValue columnName=ALGORITHM, tableName=CREDENTIAL; update tableName=CREDENTIAL		\N	4.33.0	\N	\N	7560073650
22.0.5-24031	keycloak	META-INF/jpa-changelog-22.0.0.xml	2026-04-30 14:41:17.80092	119	MARK_RAN	9:a60d2d7b315ec2d3eba9e2f145f9df28	customChange		\N	4.33.0	\N	\N	7560073650
1.8.0	mposolda@redhat.com	META-INF/db2-jpa-changelog-1.8.0.xml	2026-04-30 14:41:16.154896	21	MARK_RAN	9:831e82914316dc8a57dc09d755f23c51	addColumn tableName=IDENTITY_PROVIDER; createTable tableName=CLIENT_TEMPLATE; createTable tableName=CLIENT_TEMPLATE_ATTRIBUTES; createTable tableName=TEMPLATE_SCOPE_MAPPING; dropNotNullConstraint columnName=CLIENT_ID, tableName=PROTOCOL_MAPPER; ad...		\N	4.33.0	\N	\N	7560073650
1.8.0-2	keycloak	META-INF/db2-jpa-changelog-1.8.0.xml	2026-04-30 14:41:16.156293	22	MARK_RAN	9:f91ddca9b19743db60e3057679810e6c	dropDefaultValue columnName=ALGORITHM, tableName=CREDENTIAL; update tableName=CREDENTIAL		\N	4.33.0	\N	\N	7560073650
1.9.0	mposolda@redhat.com	META-INF/jpa-changelog-1.9.0.xml	2026-04-30 14:41:16.186811	23	EXECUTED	9:bc3d0f9e823a69dc21e23e94c7a94bb1	update tableName=REALM; update tableName=REALM; update tableName=REALM; update tableName=REALM; update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=REALM; update tableName=REALM; customChange; dr...		\N	4.33.0	\N	\N	7560073650
1.9.1	keycloak	META-INF/jpa-changelog-1.9.1.xml	2026-04-30 14:41:16.189808	24	EXECUTED	9:c9999da42f543575ab790e76439a2679	modifyDataType columnName=PRIVATE_KEY, tableName=REALM; modifyDataType columnName=PUBLIC_KEY, tableName=REALM; modifyDataType columnName=CERTIFICATE, tableName=REALM		\N	4.33.0	\N	\N	7560073650
1.9.1	keycloak	META-INF/db2-jpa-changelog-1.9.1.xml	2026-04-30 14:41:16.19073	25	MARK_RAN	9:0d6c65c6f58732d81569e77b10ba301d	modifyDataType columnName=PRIVATE_KEY, tableName=REALM; modifyDataType columnName=CERTIFICATE, tableName=REALM		\N	4.33.0	\N	\N	7560073650
1.9.2	keycloak	META-INF/jpa-changelog-1.9.2.xml	2026-04-30 14:41:16.364621	26	EXECUTED	9:fc576660fc016ae53d2d4778d84d86d0	createIndex indexName=IDX_USER_EMAIL, tableName=USER_ENTITY; createIndex indexName=IDX_USER_ROLE_MAPPING, tableName=USER_ROLE_MAPPING; createIndex indexName=IDX_USER_GROUP_MAPPING, tableName=USER_GROUP_MEMBERSHIP; createIndex indexName=IDX_USER_CO...		\N	4.33.0	\N	\N	7560073650
authz-2.0.0	psilva@redhat.com	META-INF/jpa-changelog-authz-2.0.0.xml	2026-04-30 14:41:16.399206	27	EXECUTED	9:43ed6b0da89ff77206289e87eaa9c024	createTable tableName=RESOURCE_SERVER; addPrimaryKey constraintName=CONSTRAINT_FARS, tableName=RESOURCE_SERVER; addUniqueConstraint constraintName=UK_AU8TT6T700S9V50BU18WS5HA6, tableName=RESOURCE_SERVER; createTable tableName=RESOURCE_SERVER_RESOU...		\N	4.33.0	\N	\N	7560073650
authz-2.5.1	psilva@redhat.com	META-INF/jpa-changelog-authz-2.5.1.xml	2026-04-30 14:41:16.400562	28	EXECUTED	9:44bae577f551b3738740281eceb4ea70	update tableName=RESOURCE_SERVER_POLICY		\N	4.33.0	\N	\N	7560073650
2.1.0-KEYCLOAK-5461	bburke@redhat.com	META-INF/jpa-changelog-2.1.0.xml	2026-04-30 14:41:16.421728	29	EXECUTED	9:bd88e1f833df0420b01e114533aee5e8	createTable tableName=BROKER_LINK; createTable tableName=FED_USER_ATTRIBUTE; createTable tableName=FED_USER_CONSENT; createTable tableName=FED_USER_CONSENT_ROLE; createTable tableName=FED_USER_CONSENT_PROT_MAPPER; createTable tableName=FED_USER_CR...		\N	4.33.0	\N	\N	7560073650
2.2.0	bburke@redhat.com	META-INF/jpa-changelog-2.2.0.xml	2026-04-30 14:41:16.427197	30	EXECUTED	9:a7022af5267f019d020edfe316ef4371	addColumn tableName=ADMIN_EVENT_ENTITY; createTable tableName=CREDENTIAL_ATTRIBUTE; createTable tableName=FED_CREDENTIAL_ATTRIBUTE; modifyDataType columnName=VALUE, tableName=CREDENTIAL; addForeignKeyConstraint baseTableName=FED_CREDENTIAL_ATTRIBU...		\N	4.33.0	\N	\N	7560073650
2.3.0	bburke@redhat.com	META-INF/jpa-changelog-2.3.0.xml	2026-04-30 14:41:16.432867	31	EXECUTED	9:fc155c394040654d6a79227e56f5e25a	createTable tableName=FEDERATED_USER; addPrimaryKey constraintName=CONSTR_FEDERATED_USER, tableName=FEDERATED_USER; dropDefaultValue columnName=TOTP, tableName=USER_ENTITY; dropColumn columnName=TOTP, tableName=USER_ENTITY; addColumn tableName=IDE...		\N	4.33.0	\N	\N	7560073650
2.4.0	bburke@redhat.com	META-INF/jpa-changelog-2.4.0.xml	2026-04-30 14:41:16.434587	32	EXECUTED	9:eac4ffb2a14795e5dc7b426063e54d88	customChange		\N	4.33.0	\N	\N	7560073650
2.5.0	bburke@redhat.com	META-INF/jpa-changelog-2.5.0.xml	2026-04-30 14:41:16.436359	33	EXECUTED	9:54937c05672568c4c64fc9524c1e9462	customChange; modifyDataType columnName=USER_ID, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
2.5.0-unicode-oracle	hmlnarik@redhat.com	META-INF/jpa-changelog-2.5.0.xml	2026-04-30 14:41:16.437088	34	MARK_RAN	9:f9753208029f582525ed12011a19d054	modifyDataType columnName=DESCRIPTION, tableName=AUTHENTICATION_FLOW; modifyDataType columnName=DESCRIPTION, tableName=CLIENT_TEMPLATE; modifyDataType columnName=DESCRIPTION, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=DESCRIPTION,...		\N	4.33.0	\N	\N	7560073650
2.5.0-unicode-other-dbs	hmlnarik@redhat.com	META-INF/jpa-changelog-2.5.0.xml	2026-04-30 14:41:16.447947	35	EXECUTED	9:33d72168746f81f98ae3a1e8e0ca3554	modifyDataType columnName=DESCRIPTION, tableName=AUTHENTICATION_FLOW; modifyDataType columnName=DESCRIPTION, tableName=CLIENT_TEMPLATE; modifyDataType columnName=DESCRIPTION, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=DESCRIPTION,...		\N	4.33.0	\N	\N	7560073650
2.5.0-duplicate-email-support	slawomir@dabek.name	META-INF/jpa-changelog-2.5.0.xml	2026-04-30 14:41:16.450122	36	EXECUTED	9:61b6d3d7a4c0e0024b0c839da283da0c	addColumn tableName=REALM		\N	4.33.0	\N	\N	7560073650
2.5.0-unique-group-names	hmlnarik@redhat.com	META-INF/jpa-changelog-2.5.0.xml	2026-04-30 14:41:16.454078	37	EXECUTED	9:8dcac7bdf7378e7d823cdfddebf72fda	addUniqueConstraint constraintName=SIBLING_NAMES, tableName=KEYCLOAK_GROUP		\N	4.33.0	\N	\N	7560073650
2.5.1	bburke@redhat.com	META-INF/jpa-changelog-2.5.1.xml	2026-04-30 14:41:16.455725	38	EXECUTED	9:a2b870802540cb3faa72098db5388af3	addColumn tableName=FED_USER_CONSENT		\N	4.33.0	\N	\N	7560073650
3.0.0	bburke@redhat.com	META-INF/jpa-changelog-3.0.0.xml	2026-04-30 14:41:16.457242	39	EXECUTED	9:132a67499ba24bcc54fb5cbdcfe7e4c0	addColumn tableName=IDENTITY_PROVIDER		\N	4.33.0	\N	\N	7560073650
3.2.0-fix	keycloak	META-INF/jpa-changelog-3.2.0.xml	2026-04-30 14:41:16.457793	40	MARK_RAN	9:938f894c032f5430f2b0fafb1a243462	addNotNullConstraint columnName=REALM_ID, tableName=CLIENT_INITIAL_ACCESS		\N	4.33.0	\N	\N	7560073650
3.2.0-fix-with-keycloak-5416	keycloak	META-INF/jpa-changelog-3.2.0.xml	2026-04-30 14:41:16.458484	41	MARK_RAN	9:845c332ff1874dc5d35974b0babf3006	dropIndex indexName=IDX_CLIENT_INIT_ACC_REALM, tableName=CLIENT_INITIAL_ACCESS; addNotNullConstraint columnName=REALM_ID, tableName=CLIENT_INITIAL_ACCESS; createIndex indexName=IDX_CLIENT_INIT_ACC_REALM, tableName=CLIENT_INITIAL_ACCESS		\N	4.33.0	\N	\N	7560073650
3.2.0-fix-offline-sessions	hmlnarik	META-INF/jpa-changelog-3.2.0.xml	2026-04-30 14:41:16.460431	42	EXECUTED	9:fc86359c079781adc577c5a217e4d04c	customChange		\N	4.33.0	\N	\N	7560073650
3.2.0-fixed	keycloak	META-INF/jpa-changelog-3.2.0.xml	2026-04-30 14:41:16.960001	43	EXECUTED	9:59a64800e3c0d09b825f8a3b444fa8f4	addColumn tableName=REALM; dropPrimaryKey constraintName=CONSTRAINT_OFFL_CL_SES_PK2, tableName=OFFLINE_CLIENT_SESSION; dropColumn columnName=CLIENT_SESSION_ID, tableName=OFFLINE_CLIENT_SESSION; addPrimaryKey constraintName=CONSTRAINT_OFFL_CL_SES_P...		\N	4.33.0	\N	\N	7560073650
3.3.0	keycloak	META-INF/jpa-changelog-3.3.0.xml	2026-04-30 14:41:16.961426	44	EXECUTED	9:d48d6da5c6ccf667807f633fe489ce88	addColumn tableName=USER_ENTITY		\N	4.33.0	\N	\N	7560073650
authz-3.4.0.CR1-resource-server-pk-change-part1	glavoie@gmail.com	META-INF/jpa-changelog-authz-3.4.0.CR1.xml	2026-04-30 14:41:16.962919	45	EXECUTED	9:dde36f7973e80d71fceee683bc5d2951	addColumn tableName=RESOURCE_SERVER_POLICY; addColumn tableName=RESOURCE_SERVER_RESOURCE; addColumn tableName=RESOURCE_SERVER_SCOPE		\N	4.33.0	\N	\N	7560073650
authz-3.4.0.CR1-resource-server-pk-change-part2-KEYCLOAK-6095	hmlnarik@redhat.com	META-INF/jpa-changelog-authz-3.4.0.CR1.xml	2026-04-30 14:41:16.964247	46	EXECUTED	9:b855e9b0a406b34fa323235a0cf4f640	customChange		\N	4.33.0	\N	\N	7560073650
authz-3.4.0.CR1-resource-server-pk-change-part3-fixed	glavoie@gmail.com	META-INF/jpa-changelog-authz-3.4.0.CR1.xml	2026-04-30 14:41:16.964624	47	MARK_RAN	9:51abbacd7b416c50c4421a8cabf7927e	dropIndex indexName=IDX_RES_SERV_POL_RES_SERV, tableName=RESOURCE_SERVER_POLICY; dropIndex indexName=IDX_RES_SRV_RES_RES_SRV, tableName=RESOURCE_SERVER_RESOURCE; dropIndex indexName=IDX_RES_SRV_SCOPE_RES_SRV, tableName=RESOURCE_SERVER_SCOPE		\N	4.33.0	\N	\N	7560073650
authz-3.4.0.CR1-resource-server-pk-change-part3-fixed-nodropindex	glavoie@gmail.com	META-INF/jpa-changelog-authz-3.4.0.CR1.xml	2026-04-30 14:41:17.00618	48	EXECUTED	9:bdc99e567b3398bac83263d375aad143	addNotNullConstraint columnName=RESOURCE_SERVER_CLIENT_ID, tableName=RESOURCE_SERVER_POLICY; addNotNullConstraint columnName=RESOURCE_SERVER_CLIENT_ID, tableName=RESOURCE_SERVER_RESOURCE; addNotNullConstraint columnName=RESOURCE_SERVER_CLIENT_ID, ...		\N	4.33.0	\N	\N	7560073650
authn-3.4.0.CR1-refresh-token-max-reuse	glavoie@gmail.com	META-INF/jpa-changelog-authz-3.4.0.CR1.xml	2026-04-30 14:41:17.00835	49	EXECUTED	9:d198654156881c46bfba39abd7769e69	addColumn tableName=REALM		\N	4.33.0	\N	\N	7560073650
3.4.0	keycloak	META-INF/jpa-changelog-3.4.0.xml	2026-04-30 14:41:17.021696	50	EXECUTED	9:cfdd8736332ccdd72c5256ccb42335db	addPrimaryKey constraintName=CONSTRAINT_REALM_DEFAULT_ROLES, tableName=REALM_DEFAULT_ROLES; addPrimaryKey constraintName=CONSTRAINT_COMPOSITE_ROLE, tableName=COMPOSITE_ROLE; addPrimaryKey constraintName=CONSTR_REALM_DEFAULT_GROUPS, tableName=REALM...		\N	4.33.0	\N	\N	7560073650
3.4.0-KEYCLOAK-5230	hmlnarik@redhat.com	META-INF/jpa-changelog-3.4.0.xml	2026-04-30 14:41:17.167025	51	EXECUTED	9:7c84de3d9bd84d7f077607c1a4dcb714	createIndex indexName=IDX_FU_ATTRIBUTE, tableName=FED_USER_ATTRIBUTE; createIndex indexName=IDX_FU_CONSENT, tableName=FED_USER_CONSENT; createIndex indexName=IDX_FU_CONSENT_RU, tableName=FED_USER_CONSENT; createIndex indexName=IDX_FU_CREDENTIAL, t...		\N	4.33.0	\N	\N	7560073650
3.4.1	psilva@redhat.com	META-INF/jpa-changelog-3.4.1.xml	2026-04-30 14:41:17.168408	52	EXECUTED	9:5a6bb36cbefb6a9d6928452c0852af2d	modifyDataType columnName=VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
3.4.2	keycloak	META-INF/jpa-changelog-3.4.2.xml	2026-04-30 14:41:17.169836	53	EXECUTED	9:8f23e334dbc59f82e0a328373ca6ced0	update tableName=REALM		\N	4.33.0	\N	\N	7560073650
3.4.2-KEYCLOAK-5172	mkanis@redhat.com	META-INF/jpa-changelog-3.4.2.xml	2026-04-30 14:41:17.17177	54	EXECUTED	9:9156214268f09d970cdf0e1564d866af	update tableName=CLIENT		\N	4.33.0	\N	\N	7560073650
4.0.0-KEYCLOAK-6335	bburke@redhat.com	META-INF/jpa-changelog-4.0.0.xml	2026-04-30 14:41:17.184053	55	EXECUTED	9:db806613b1ed154826c02610b7dbdf74	createTable tableName=CLIENT_AUTH_FLOW_BINDINGS; addPrimaryKey constraintName=C_CLI_FLOW_BIND, tableName=CLIENT_AUTH_FLOW_BINDINGS		\N	4.33.0	\N	\N	7560073650
4.0.0-CLEANUP-UNUSED-TABLE	bburke@redhat.com	META-INF/jpa-changelog-4.0.0.xml	2026-04-30 14:41:17.191353	56	EXECUTED	9:229a041fb72d5beac76bb94a5fa709de	dropTable tableName=CLIENT_IDENTITY_PROV_MAPPING		\N	4.33.0	\N	\N	7560073650
4.0.0-KEYCLOAK-6228	bburke@redhat.com	META-INF/jpa-changelog-4.0.0.xml	2026-04-30 14:41:17.210632	57	EXECUTED	9:079899dade9c1e683f26b2aa9ca6ff04	dropUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHOGM8UEWRT, tableName=USER_CONSENT; dropNotNullConstraint columnName=CLIENT_ID, tableName=USER_CONSENT; addColumn tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHO...		\N	4.33.0	\N	\N	7560073650
4.0.0-KEYCLOAK-5579-fixed	mposolda@redhat.com	META-INF/jpa-changelog-4.0.0.xml	2026-04-30 14:41:17.369626	58	EXECUTED	9:139b79bcbbfe903bb1c2d2a4dbf001d9	dropForeignKeyConstraint baseTableName=CLIENT_TEMPLATE_ATTRIBUTES, constraintName=FK_CL_TEMPL_ATTR_TEMPL; renameTable newTableName=CLIENT_SCOPE_ATTRIBUTES, oldTableName=CLIENT_TEMPLATE_ATTRIBUTES; renameColumn newColumnName=SCOPE_ID, oldColumnName...		\N	4.33.0	\N	\N	7560073650
authz-4.0.0.CR1	psilva@redhat.com	META-INF/jpa-changelog-authz-4.0.0.CR1.xml	2026-04-30 14:41:17.378103	59	EXECUTED	9:b55738ad889860c625ba2bf483495a04	createTable tableName=RESOURCE_SERVER_PERM_TICKET; addPrimaryKey constraintName=CONSTRAINT_FAPMT, tableName=RESOURCE_SERVER_PERM_TICKET; addForeignKeyConstraint baseTableName=RESOURCE_SERVER_PERM_TICKET, constraintName=FK_FRSRHO213XCX4WNKOG82SSPMT...		\N	4.33.0	\N	\N	7560073650
authz-4.0.0.Beta3	psilva@redhat.com	META-INF/jpa-changelog-authz-4.0.0.Beta3.xml	2026-04-30 14:41:17.379918	60	EXECUTED	9:e0057eac39aa8fc8e09ac6cfa4ae15fe	addColumn tableName=RESOURCE_SERVER_POLICY; addColumn tableName=RESOURCE_SERVER_PERM_TICKET; addForeignKeyConstraint baseTableName=RESOURCE_SERVER_PERM_TICKET, constraintName=FK_FRSRPO2128CX4WNKOG82SSRFY, referencedTableName=RESOURCE_SERVER_POLICY		\N	4.33.0	\N	\N	7560073650
authz-4.2.0.Final	mhajas@redhat.com	META-INF/jpa-changelog-authz-4.2.0.Final.xml	2026-04-30 14:41:17.382572	61	EXECUTED	9:42a33806f3a0443fe0e7feeec821326c	createTable tableName=RESOURCE_URIS; addForeignKeyConstraint baseTableName=RESOURCE_URIS, constraintName=FK_RESOURCE_SERVER_URIS, referencedTableName=RESOURCE_SERVER_RESOURCE; customChange; dropColumn columnName=URI, tableName=RESOURCE_SERVER_RESO...		\N	4.33.0	\N	\N	7560073650
authz-4.2.0.Final-KEYCLOAK-9944	hmlnarik@redhat.com	META-INF/jpa-changelog-authz-4.2.0.Final.xml	2026-04-30 14:41:17.383972	62	EXECUTED	9:9968206fca46eecc1f51db9c024bfe56	addPrimaryKey constraintName=CONSTRAINT_RESOUR_URIS_PK, tableName=RESOURCE_URIS		\N	4.33.0	\N	\N	7560073650
4.2.0-KEYCLOAK-6313	wadahiro@gmail.com	META-INF/jpa-changelog-4.2.0.xml	2026-04-30 14:41:17.384907	63	EXECUTED	9:92143a6daea0a3f3b8f598c97ce55c3d	addColumn tableName=REQUIRED_ACTION_PROVIDER		\N	4.33.0	\N	\N	7560073650
4.3.0-KEYCLOAK-7984	wadahiro@gmail.com	META-INF/jpa-changelog-4.3.0.xml	2026-04-30 14:41:17.385721	64	EXECUTED	9:82bab26a27195d889fb0429003b18f40	update tableName=REQUIRED_ACTION_PROVIDER		\N	4.33.0	\N	\N	7560073650
4.6.0-KEYCLOAK-7950	psilva@redhat.com	META-INF/jpa-changelog-4.6.0.xml	2026-04-30 14:41:17.38654	65	EXECUTED	9:e590c88ddc0b38b0ae4249bbfcb5abc3	update tableName=RESOURCE_SERVER_RESOURCE		\N	4.33.0	\N	\N	7560073650
4.6.0-KEYCLOAK-8377	keycloak	META-INF/jpa-changelog-4.6.0.xml	2026-04-30 14:41:17.403326	66	EXECUTED	9:5c1f475536118dbdc38d5d7977950cc0	createTable tableName=ROLE_ATTRIBUTE; addPrimaryKey constraintName=CONSTRAINT_ROLE_ATTRIBUTE_PK, tableName=ROLE_ATTRIBUTE; addForeignKeyConstraint baseTableName=ROLE_ATTRIBUTE, constraintName=FK_ROLE_ATTRIBUTE_ID, referencedTableName=KEYCLOAK_ROLE...		\N	4.33.0	\N	\N	7560073650
4.6.0-KEYCLOAK-8555	gideonray@gmail.com	META-INF/jpa-changelog-4.6.0.xml	2026-04-30 14:41:17.418116	67	EXECUTED	9:e7c9f5f9c4d67ccbbcc215440c718a17	createIndex indexName=IDX_COMPONENT_PROVIDER_TYPE, tableName=COMPONENT		\N	4.33.0	\N	\N	7560073650
4.7.0-KEYCLOAK-1267	sguilhen@redhat.com	META-INF/jpa-changelog-4.7.0.xml	2026-04-30 14:41:17.41986	68	EXECUTED	9:88e0bfdda924690d6f4e430c53447dd5	addColumn tableName=REALM		\N	4.33.0	\N	\N	7560073650
4.7.0-KEYCLOAK-7275	keycloak	META-INF/jpa-changelog-4.7.0.xml	2026-04-30 14:41:17.437203	69	EXECUTED	9:f53177f137e1c46b6a88c59ec1cb5218	renameColumn newColumnName=CREATED_ON, oldColumnName=LAST_SESSION_REFRESH, tableName=OFFLINE_USER_SESSION; addNotNullConstraint columnName=CREATED_ON, tableName=OFFLINE_USER_SESSION; addColumn tableName=OFFLINE_USER_SESSION; customChange; createIn...		\N	4.33.0	\N	\N	7560073650
4.8.0-KEYCLOAK-8835	sguilhen@redhat.com	META-INF/jpa-changelog-4.8.0.xml	2026-04-30 14:41:17.438904	70	EXECUTED	9:a74d33da4dc42a37ec27121580d1459f	addNotNullConstraint columnName=SSO_MAX_LIFESPAN_REMEMBER_ME, tableName=REALM; addNotNullConstraint columnName=SSO_IDLE_TIMEOUT_REMEMBER_ME, tableName=REALM		\N	4.33.0	\N	\N	7560073650
authz-7.0.0-KEYCLOAK-10443	psilva@redhat.com	META-INF/jpa-changelog-authz-7.0.0.xml	2026-04-30 14:41:17.440199	71	EXECUTED	9:fd4ade7b90c3b67fae0bfcfcb42dfb5f	addColumn tableName=RESOURCE_SERVER		\N	4.33.0	\N	\N	7560073650
8.0.0-adding-credential-columns	keycloak	META-INF/jpa-changelog-8.0.0.xml	2026-04-30 14:41:17.442373	72	EXECUTED	9:aa072ad090bbba210d8f18781b8cebf4	addColumn tableName=CREDENTIAL; addColumn tableName=FED_USER_CREDENTIAL		\N	4.33.0	\N	\N	7560073650
8.0.0-updating-credential-data-not-oracle-fixed	keycloak	META-INF/jpa-changelog-8.0.0.xml	2026-04-30 14:41:17.444831	73	EXECUTED	9:1ae6be29bab7c2aa376f6983b932be37	update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=FED_USER_CREDENTIAL; update tableName=FED_USER_CREDENTIAL; update tableName=FED_USER_CREDENTIAL		\N	4.33.0	\N	\N	7560073650
8.0.0-updating-credential-data-oracle-fixed	keycloak	META-INF/jpa-changelog-8.0.0.xml	2026-04-30 14:41:17.445689	74	MARK_RAN	9:14706f286953fc9a25286dbd8fb30d97	update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=CREDENTIAL; update tableName=FED_USER_CREDENTIAL; update tableName=FED_USER_CREDENTIAL; update tableName=FED_USER_CREDENTIAL		\N	4.33.0	\N	\N	7560073650
8.0.0-credential-cleanup-fixed	keycloak	META-INF/jpa-changelog-8.0.0.xml	2026-04-30 14:41:17.451433	75	EXECUTED	9:2b9cc12779be32c5b40e2e67711a218b	dropDefaultValue columnName=COUNTER, tableName=CREDENTIAL; dropDefaultValue columnName=DIGITS, tableName=CREDENTIAL; dropDefaultValue columnName=PERIOD, tableName=CREDENTIAL; dropDefaultValue columnName=ALGORITHM, tableName=CREDENTIAL; dropColumn ...		\N	4.33.0	\N	\N	7560073650
8.0.0-resource-tag-support	keycloak	META-INF/jpa-changelog-8.0.0.xml	2026-04-30 14:41:17.467948	76	EXECUTED	9:91fa186ce7a5af127a2d7a91ee083cc5	addColumn tableName=MIGRATION_MODEL; createIndex indexName=IDX_UPDATE_TIME, tableName=MIGRATION_MODEL		\N	4.33.0	\N	\N	7560073650
9.0.0-always-display-client	keycloak	META-INF/jpa-changelog-9.0.0.xml	2026-04-30 14:41:17.469266	77	EXECUTED	9:6335e5c94e83a2639ccd68dd24e2e5ad	addColumn tableName=CLIENT		\N	4.33.0	\N	\N	7560073650
9.0.0-drop-constraints-for-column-increase	keycloak	META-INF/jpa-changelog-9.0.0.xml	2026-04-30 14:41:17.469808	78	MARK_RAN	9:6bdb5658951e028bfe16fa0a8228b530	dropUniqueConstraint constraintName=UK_FRSR6T700S9V50BU18WS5PMT, tableName=RESOURCE_SERVER_PERM_TICKET; dropUniqueConstraint constraintName=UK_FRSR6T700S9V50BU18WS5HA6, tableName=RESOURCE_SERVER_RESOURCE; dropPrimaryKey constraintName=CONSTRAINT_O...		\N	4.33.0	\N	\N	7560073650
9.0.0-increase-column-size-federated-fk	keycloak	META-INF/jpa-changelog-9.0.0.xml	2026-04-30 14:41:17.475303	79	EXECUTED	9:d5bc15a64117ccad481ce8792d4c608f	modifyDataType columnName=CLIENT_ID, tableName=FED_USER_CONSENT; modifyDataType columnName=CLIENT_REALM_CONSTRAINT, tableName=KEYCLOAK_ROLE; modifyDataType columnName=OWNER, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=CLIENT_ID, ta...		\N	4.33.0	\N	\N	7560073650
9.0.0-recreate-constraints-after-column-increase	keycloak	META-INF/jpa-changelog-9.0.0.xml	2026-04-30 14:41:17.475939	80	MARK_RAN	9:077cba51999515f4d3e7ad5619ab592c	addNotNullConstraint columnName=CLIENT_ID, tableName=OFFLINE_CLIENT_SESSION; addNotNullConstraint columnName=OWNER, tableName=RESOURCE_SERVER_PERM_TICKET; addNotNullConstraint columnName=REQUESTER, tableName=RESOURCE_SERVER_PERM_TICKET; addNotNull...		\N	4.33.0	\N	\N	7560073650
9.0.1-add-index-to-client.client_id	keycloak	META-INF/jpa-changelog-9.0.1.xml	2026-04-30 14:41:17.49321	81	EXECUTED	9:be969f08a163bf47c6b9e9ead8ac2afb	createIndex indexName=IDX_CLIENT_ID, tableName=CLIENT		\N	4.33.0	\N	\N	7560073650
9.0.1-KEYCLOAK-12579-drop-constraints	keycloak	META-INF/jpa-changelog-9.0.1.xml	2026-04-30 14:41:17.493873	82	MARK_RAN	9:6d3bb4408ba5a72f39bd8a0b301ec6e3	dropUniqueConstraint constraintName=SIBLING_NAMES, tableName=KEYCLOAK_GROUP		\N	4.33.0	\N	\N	7560073650
9.0.1-KEYCLOAK-12579-add-not-null-constraint	keycloak	META-INF/jpa-changelog-9.0.1.xml	2026-04-30 14:41:17.49541	83	EXECUTED	9:966bda61e46bebf3cc39518fbed52fa7	addNotNullConstraint columnName=PARENT_GROUP, tableName=KEYCLOAK_GROUP		\N	4.33.0	\N	\N	7560073650
9.0.1-KEYCLOAK-12579-recreate-constraints	keycloak	META-INF/jpa-changelog-9.0.1.xml	2026-04-30 14:41:17.495904	84	MARK_RAN	9:8dcac7bdf7378e7d823cdfddebf72fda	addUniqueConstraint constraintName=SIBLING_NAMES, tableName=KEYCLOAK_GROUP		\N	4.33.0	\N	\N	7560073650
9.0.1-add-index-to-events	keycloak	META-INF/jpa-changelog-9.0.1.xml	2026-04-30 14:41:17.512228	85	EXECUTED	9:7d93d602352a30c0c317e6a609b56599	createIndex indexName=IDX_EVENT_TIME, tableName=EVENT_ENTITY		\N	4.33.0	\N	\N	7560073650
map-remove-ri	keycloak	META-INF/jpa-changelog-11.0.0.xml	2026-04-30 14:41:17.514008	86	EXECUTED	9:71c5969e6cdd8d7b6f47cebc86d37627	dropForeignKeyConstraint baseTableName=REALM, constraintName=FK_TRAF444KK6QRKMS7N56AIWQ5Y; dropForeignKeyConstraint baseTableName=KEYCLOAK_ROLE, constraintName=FK_KJHO5LE2C0RAL09FL8CM9WFW9		\N	4.33.0	\N	\N	7560073650
map-remove-ri	keycloak	META-INF/jpa-changelog-12.0.0.xml	2026-04-30 14:41:17.516449	87	EXECUTED	9:a9ba7d47f065f041b7da856a81762021	dropForeignKeyConstraint baseTableName=REALM_DEFAULT_GROUPS, constraintName=FK_DEF_GROUPS_GROUP; dropForeignKeyConstraint baseTableName=REALM_DEFAULT_ROLES, constraintName=FK_H4WPD7W4HSOOLNI3H0SW7BTJE; dropForeignKeyConstraint baseTableName=CLIENT...		\N	4.33.0	\N	\N	7560073650
12.1.0-add-realm-localization-table	keycloak	META-INF/jpa-changelog-12.0.0.xml	2026-04-30 14:41:17.519952	88	EXECUTED	9:fffabce2bc01e1a8f5110d5278500065	createTable tableName=REALM_LOCALIZATIONS; addPrimaryKey tableName=REALM_LOCALIZATIONS		\N	4.33.0	\N	\N	7560073650
default-roles	keycloak	META-INF/jpa-changelog-13.0.0.xml	2026-04-30 14:41:17.522022	89	EXECUTED	9:fa8a5b5445e3857f4b010bafb5009957	addColumn tableName=REALM; customChange		\N	4.33.0	\N	\N	7560073650
default-roles-cleanup	keycloak	META-INF/jpa-changelog-13.0.0.xml	2026-04-30 14:41:17.523842	90	EXECUTED	9:67ac3241df9a8582d591c5ed87125f39	dropTable tableName=REALM_DEFAULT_ROLES; dropTable tableName=CLIENT_DEFAULT_ROLES		\N	4.33.0	\N	\N	7560073650
13.0.0-KEYCLOAK-16844	keycloak	META-INF/jpa-changelog-13.0.0.xml	2026-04-30 14:41:17.538685	91	EXECUTED	9:ad1194d66c937e3ffc82386c050ba089	createIndex indexName=IDX_OFFLINE_USS_PRELOAD, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
map-remove-ri-13.0.0	keycloak	META-INF/jpa-changelog-13.0.0.xml	2026-04-30 14:41:17.541153	92	EXECUTED	9:d9be619d94af5a2f5d07b9f003543b91	dropForeignKeyConstraint baseTableName=DEFAULT_CLIENT_SCOPE, constraintName=FK_R_DEF_CLI_SCOPE_SCOPE; dropForeignKeyConstraint baseTableName=CLIENT_SCOPE_CLIENT, constraintName=FK_C_CLI_SCOPE_SCOPE; dropForeignKeyConstraint baseTableName=CLIENT_SC...		\N	4.33.0	\N	\N	7560073650
13.0.0-KEYCLOAK-17992-drop-constraints	keycloak	META-INF/jpa-changelog-13.0.0.xml	2026-04-30 14:41:17.541639	93	MARK_RAN	9:544d201116a0fcc5a5da0925fbbc3bde	dropPrimaryKey constraintName=C_CLI_SCOPE_BIND, tableName=CLIENT_SCOPE_CLIENT; dropIndex indexName=IDX_CLSCOPE_CL, tableName=CLIENT_SCOPE_CLIENT; dropIndex indexName=IDX_CL_CLSCOPE, tableName=CLIENT_SCOPE_CLIENT		\N	4.33.0	\N	\N	7560073650
13.0.0-increase-column-size-federated	keycloak	META-INF/jpa-changelog-13.0.0.xml	2026-04-30 14:41:17.544073	94	EXECUTED	9:43c0c1055b6761b4b3e89de76d612ccf	modifyDataType columnName=CLIENT_ID, tableName=CLIENT_SCOPE_CLIENT; modifyDataType columnName=SCOPE_ID, tableName=CLIENT_SCOPE_CLIENT		\N	4.33.0	\N	\N	7560073650
13.0.0-KEYCLOAK-17992-recreate-constraints	keycloak	META-INF/jpa-changelog-13.0.0.xml	2026-04-30 14:41:17.544627	95	MARK_RAN	9:8bd711fd0330f4fe980494ca43ab1139	addNotNullConstraint columnName=CLIENT_ID, tableName=CLIENT_SCOPE_CLIENT; addNotNullConstraint columnName=SCOPE_ID, tableName=CLIENT_SCOPE_CLIENT; addPrimaryKey constraintName=C_CLI_SCOPE_BIND, tableName=CLIENT_SCOPE_CLIENT; createIndex indexName=...		\N	4.33.0	\N	\N	7560073650
json-string-accomodation-fixed	keycloak	META-INF/jpa-changelog-13.0.0.xml	2026-04-30 14:41:17.546506	96	EXECUTED	9:e07d2bc0970c348bb06fb63b1f82ddbf	addColumn tableName=REALM_ATTRIBUTE; update tableName=REALM_ATTRIBUTE; dropColumn columnName=VALUE, tableName=REALM_ATTRIBUTE; renameColumn newColumnName=VALUE, oldColumnName=VALUE_NEW, tableName=REALM_ATTRIBUTE		\N	4.33.0	\N	\N	7560073650
14.0.0-KEYCLOAK-11019	keycloak	META-INF/jpa-changelog-14.0.0.xml	2026-04-30 14:41:17.600472	97	EXECUTED	9:24fb8611e97f29989bea412aa38d12b7	createIndex indexName=IDX_OFFLINE_CSS_PRELOAD, tableName=OFFLINE_CLIENT_SESSION; createIndex indexName=IDX_OFFLINE_USS_BY_USER, tableName=OFFLINE_USER_SESSION; createIndex indexName=IDX_OFFLINE_USS_BY_USERSESS, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
14.0.0-KEYCLOAK-18286	keycloak	META-INF/jpa-changelog-14.0.0.xml	2026-04-30 14:41:17.601178	98	MARK_RAN	9:259f89014ce2506ee84740cbf7163aa7	createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
14.0.0-KEYCLOAK-18286-revert	keycloak	META-INF/jpa-changelog-14.0.0.xml	2026-04-30 14:41:17.606692	99	MARK_RAN	9:04baaf56c116ed19951cbc2cca584022	dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
14.0.0-KEYCLOAK-18286-supported-dbs	keycloak	META-INF/jpa-changelog-14.0.0.xml	2026-04-30 14:41:17.624696	100	EXECUTED	9:60ca84a0f8c94ec8c3504a5a3bc88ee8	createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
14.0.0-KEYCLOAK-18286-unsupported-dbs	keycloak	META-INF/jpa-changelog-14.0.0.xml	2026-04-30 14:41:17.625533	101	MARK_RAN	9:d3d977031d431db16e2c181ce49d73e9	createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
KEYCLOAK-17267-add-index-to-user-attributes	keycloak	META-INF/jpa-changelog-14.0.0.xml	2026-04-30 14:41:17.653653	102	EXECUTED	9:0b305d8d1277f3a89a0a53a659ad274c	createIndex indexName=IDX_USER_ATTRIBUTE_NAME, tableName=USER_ATTRIBUTE		\N	4.33.0	\N	\N	7560073650
KEYCLOAK-18146-add-saml-art-binding-identifier	keycloak	META-INF/jpa-changelog-14.0.0.xml	2026-04-30 14:41:17.655606	103	EXECUTED	9:2c374ad2cdfe20e2905a84c8fac48460	customChange		\N	4.33.0	\N	\N	7560073650
15.0.0-KEYCLOAK-18467	keycloak	META-INF/jpa-changelog-15.0.0.xml	2026-04-30 14:41:17.658075	104	EXECUTED	9:47a760639ac597360a8219f5b768b4de	addColumn tableName=REALM_LOCALIZATIONS; update tableName=REALM_LOCALIZATIONS; dropColumn columnName=TEXTS, tableName=REALM_LOCALIZATIONS; renameColumn newColumnName=TEXTS, oldColumnName=TEXTS_NEW, tableName=REALM_LOCALIZATIONS; addNotNullConstrai...		\N	4.33.0	\N	\N	7560073650
17.0.0-9562	keycloak	META-INF/jpa-changelog-17.0.0.xml	2026-04-30 14:41:17.677344	105	EXECUTED	9:a6272f0576727dd8cad2522335f5d99e	createIndex indexName=IDX_USER_SERVICE_ACCOUNT, tableName=USER_ENTITY		\N	4.33.0	\N	\N	7560073650
18.0.0-10625-IDX_ADMIN_EVENT_TIME	keycloak	META-INF/jpa-changelog-18.0.0.xml	2026-04-30 14:41:17.697548	106	EXECUTED	9:015479dbd691d9cc8669282f4828c41d	createIndex indexName=IDX_ADMIN_EVENT_TIME, tableName=ADMIN_EVENT_ENTITY		\N	4.33.0	\N	\N	7560073650
18.0.15-30992-index-consent	keycloak	META-INF/jpa-changelog-18.0.15.xml	2026-04-30 14:41:17.722174	107	EXECUTED	9:80071ede7a05604b1f4906f3bf3b00f0	createIndex indexName=IDX_USCONSENT_SCOPE_ID, tableName=USER_CONSENT_CLIENT_SCOPE		\N	4.33.0	\N	\N	7560073650
19.0.0-10135	keycloak	META-INF/jpa-changelog-19.0.0.xml	2026-04-30 14:41:17.725507	108	EXECUTED	9:9518e495fdd22f78ad6425cc30630221	customChange		\N	4.33.0	\N	\N	7560073650
20.0.0-12964-supported-dbs	keycloak	META-INF/jpa-changelog-20.0.0.xml	2026-04-30 14:41:17.748144	109	EXECUTED	9:e5f243877199fd96bcc842f27a1656ac	createIndex indexName=IDX_GROUP_ATT_BY_NAME_VALUE, tableName=GROUP_ATTRIBUTE		\N	4.33.0	\N	\N	7560073650
20.0.0-12964-supported-dbs-edb-migration	keycloak	META-INF/jpa-changelog-20.0.0.xml	2026-04-30 14:41:17.774396	110	EXECUTED	9:a6b18a8e38062df5793edbe064f4aecd	dropIndex indexName=IDX_GROUP_ATT_BY_NAME_VALUE, tableName=GROUP_ATTRIBUTE; createIndex indexName=IDX_GROUP_ATT_BY_NAME_VALUE, tableName=GROUP_ATTRIBUTE		\N	4.33.0	\N	\N	7560073650
20.0.0-12964-unsupported-dbs	keycloak	META-INF/jpa-changelog-20.0.0.xml	2026-04-30 14:41:17.775278	111	MARK_RAN	9:1a6fcaa85e20bdeae0a9ce49b41946a5	createIndex indexName=IDX_GROUP_ATT_BY_NAME_VALUE, tableName=GROUP_ATTRIBUTE		\N	4.33.0	\N	\N	7560073650
client-attributes-string-accomodation-fixed-pre-drop-index	keycloak	META-INF/jpa-changelog-20.0.0.xml	2026-04-30 14:41:17.776701	112	EXECUTED	9:04baaf56c116ed19951cbc2cca584022	dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
client-attributes-string-accomodation-fixed	keycloak	META-INF/jpa-changelog-20.0.0.xml	2026-04-30 14:41:17.778686	113	EXECUTED	9:3f332e13e90739ed0c35b0b25b7822ca	addColumn tableName=CLIENT_ATTRIBUTES; update tableName=CLIENT_ATTRIBUTES; dropColumn columnName=VALUE, tableName=CLIENT_ATTRIBUTES; renameColumn newColumnName=VALUE, oldColumnName=VALUE_NEW, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
client-attributes-string-accomodation-fixed-post-create-index	keycloak	META-INF/jpa-changelog-20.0.0.xml	2026-04-30 14:41:17.779314	114	MARK_RAN	9:bd2bd0fc7768cf0845ac96a8786fa735	createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
21.0.2-17277	keycloak	META-INF/jpa-changelog-21.0.2.xml	2026-04-30 14:41:17.780963	115	EXECUTED	9:7ee1f7a3fb8f5588f171fb9a6ab623c0	customChange		\N	4.33.0	\N	\N	7560073650
21.1.0-19404	keycloak	META-INF/jpa-changelog-21.1.0.xml	2026-04-30 14:41:17.796195	116	EXECUTED	9:3d7e830b52f33676b9d64f7f2b2ea634	modifyDataType columnName=DECISION_STRATEGY, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=LOGIC, tableName=RESOURCE_SERVER_POLICY; modifyDataType columnName=POLICY_ENFORCE_MODE, tableName=RESOURCE_SERVER		\N	4.33.0	\N	\N	7560073650
21.1.0-19404-2	keycloak	META-INF/jpa-changelog-21.1.0.xml	2026-04-30 14:41:17.797849	117	MARK_RAN	9:627d032e3ef2c06c0e1f73d2ae25c26c	addColumn tableName=RESOURCE_SERVER_POLICY; update tableName=RESOURCE_SERVER_POLICY; dropColumn columnName=DECISION_STRATEGY, tableName=RESOURCE_SERVER_POLICY; renameColumn newColumnName=DECISION_STRATEGY, oldColumnName=DECISION_STRATEGY_NEW, tabl...		\N	4.33.0	\N	\N	7560073650
22.0.0-17484-updated	keycloak	META-INF/jpa-changelog-22.0.0.xml	2026-04-30 14:41:17.800235	118	EXECUTED	9:90af0bfd30cafc17b9f4d6eccd92b8b3	customChange		\N	4.33.0	\N	\N	7560073650
23.0.0-12062	keycloak	META-INF/jpa-changelog-23.0.0.xml	2026-04-30 14:41:17.804351	120	EXECUTED	9:2168fbe728fec46ae9baf15bf80927b8	addColumn tableName=COMPONENT_CONFIG; update tableName=COMPONENT_CONFIG; dropColumn columnName=VALUE, tableName=COMPONENT_CONFIG; renameColumn newColumnName=VALUE, oldColumnName=VALUE_NEW, tableName=COMPONENT_CONFIG		\N	4.33.0	\N	\N	7560073650
23.0.0-17258	keycloak	META-INF/jpa-changelog-23.0.0.xml	2026-04-30 14:41:17.805782	121	EXECUTED	9:36506d679a83bbfda85a27ea1864dca8	addColumn tableName=EVENT_ENTITY		\N	4.33.0	\N	\N	7560073650
24.0.0-9758	keycloak	META-INF/jpa-changelog-24.0.0.xml	2026-04-30 14:41:17.886931	122	EXECUTED	9:502c557a5189f600f0f445a9b49ebbce	addColumn tableName=USER_ATTRIBUTE; addColumn tableName=FED_USER_ATTRIBUTE; createIndex indexName=USER_ATTR_LONG_VALUES, tableName=USER_ATTRIBUTE; createIndex indexName=FED_USER_ATTR_LONG_VALUES, tableName=FED_USER_ATTRIBUTE; createIndex indexName...		\N	4.33.0	\N	\N	7560073650
24.0.0-9758-2	keycloak	META-INF/jpa-changelog-24.0.0.xml	2026-04-30 14:41:17.888658	123	EXECUTED	9:bf0fdee10afdf597a987adbf291db7b2	customChange		\N	4.33.0	\N	\N	7560073650
24.0.0-26618-drop-index-if-present	keycloak	META-INF/jpa-changelog-24.0.0.xml	2026-04-30 14:41:17.890787	124	MARK_RAN	9:04baaf56c116ed19951cbc2cca584022	dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
24.0.0-26618-reindex	keycloak	META-INF/jpa-changelog-24.0.0.xml	2026-04-30 14:41:17.914372	125	EXECUTED	9:08707c0f0db1cef6b352db03a60edc7f	createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
24.0.0-26618-edb-migration	keycloak	META-INF/jpa-changelog-24.0.0.xml	2026-04-30 14:41:17.945016	126	EXECUTED	9:2f684b29d414cd47efe3a3599f390741	dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES; createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
24.0.2-27228	keycloak	META-INF/jpa-changelog-24.0.2.xml	2026-04-30 14:41:17.947333	127	EXECUTED	9:eaee11f6b8aa25d2cc6a84fb86fc6238	customChange		\N	4.33.0	\N	\N	7560073650
24.0.2-27967-drop-index-if-present	keycloak	META-INF/jpa-changelog-24.0.2.xml	2026-04-30 14:41:17.94815	128	MARK_RAN	9:04baaf56c116ed19951cbc2cca584022	dropIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
24.0.2-27967-reindex	keycloak	META-INF/jpa-changelog-24.0.2.xml	2026-04-30 14:41:17.94958	129	MARK_RAN	9:d3d977031d431db16e2c181ce49d73e9	createIndex indexName=IDX_CLIENT_ATT_BY_NAME_VALUE, tableName=CLIENT_ATTRIBUTES		\N	4.33.0	\N	\N	7560073650
25.0.0-28265-tables	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:17.952614	130	EXECUTED	9:deda2df035df23388af95bbd36c17cef	addColumn tableName=OFFLINE_USER_SESSION; addColumn tableName=OFFLINE_CLIENT_SESSION		\N	4.33.0	\N	\N	7560073650
25.0.0-28265-index-creation	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:17.973177	131	EXECUTED	9:3e96709818458ae49f3c679ae58d263a	createIndex indexName=IDX_OFFLINE_USS_BY_LAST_SESSION_REFRESH, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
25.0.0-28265-index-cleanup-uss-createdon	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:17.976645	132	EXECUTED	9:78ab4fc129ed5e8265dbcc3485fba92f	dropIndex indexName=IDX_OFFLINE_USS_CREATEDON, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
25.0.0-28265-index-cleanup-uss-preload	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:17.97923	133	EXECUTED	9:de5f7c1f7e10994ed8b62e621d20eaab	dropIndex indexName=IDX_OFFLINE_USS_PRELOAD, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
25.0.0-28265-index-cleanup-uss-by-usersess	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:17.982013	134	EXECUTED	9:6eee220d024e38e89c799417ec33667f	dropIndex indexName=IDX_OFFLINE_USS_BY_USERSESS, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
25.0.0-28265-index-cleanup-css-preload	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:17.986479	135	EXECUTED	9:5411d2fb2891d3e8d63ddb55dfa3c0c9	dropIndex indexName=IDX_OFFLINE_CSS_PRELOAD, tableName=OFFLINE_CLIENT_SESSION		\N	4.33.0	\N	\N	7560073650
25.0.0-28265-index-2-mysql	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:17.987402	136	MARK_RAN	9:b7ef76036d3126bb83c2423bf4d449d6	createIndex indexName=IDX_OFFLINE_USS_BY_BROKER_SESSION_ID, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
25.0.0-28265-index-2-not-mysql	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:18.004725	137	EXECUTED	9:23396cf51ab8bc1ae6f0cac7f9f6fcf7	createIndex indexName=IDX_OFFLINE_USS_BY_BROKER_SESSION_ID, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
25.0.0-org	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:18.015343	138	EXECUTED	9:5c859965c2c9b9c72136c360649af157	createTable tableName=ORG; addUniqueConstraint constraintName=UK_ORG_NAME, tableName=ORG; addUniqueConstraint constraintName=UK_ORG_GROUP, tableName=ORG; createTable tableName=ORG_DOMAIN		\N	4.33.0	\N	\N	7560073650
unique-consentuser	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:18.019456	139	EXECUTED	9:5857626a2ea8767e9a6c66bf3a2cb32f	customChange; dropUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHOGM8UEWRT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_LOCAL_CONSENT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_EXTERNAL_CONSENT, tableName=...		\N	4.33.0	\N	\N	7560073650
unique-consentuser-edb-migration	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:18.023394	140	MARK_RAN	9:5857626a2ea8767e9a6c66bf3a2cb32f	customChange; dropUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHOGM8UEWRT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_LOCAL_CONSENT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_EXTERNAL_CONSENT, tableName=...		\N	4.33.0	\N	\N	7560073650
unique-consentuser-mysql	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:18.024542	141	MARK_RAN	9:b79478aad5adaa1bc428e31563f55e8e	customChange; dropUniqueConstraint constraintName=UK_JKUWUVD56ONTGSUHOGM8UEWRT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_LOCAL_CONSENT, tableName=USER_CONSENT; addUniqueConstraint constraintName=UK_EXTERNAL_CONSENT, tableName=...		\N	4.33.0	\N	\N	7560073650
25.0.0-28861-index-creation	keycloak	META-INF/jpa-changelog-25.0.0.xml	2026-04-30 14:41:18.060612	142	EXECUTED	9:b9acb58ac958d9ada0fe12a5d4794ab1	createIndex indexName=IDX_PERM_TICKET_REQUESTER, tableName=RESOURCE_SERVER_PERM_TICKET; createIndex indexName=IDX_PERM_TICKET_OWNER, tableName=RESOURCE_SERVER_PERM_TICKET		\N	4.33.0	\N	\N	7560073650
26.0.0-org-alias	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.063429	143	EXECUTED	9:6ef7d63e4412b3c2d66ed179159886a4	addColumn tableName=ORG; update tableName=ORG; addNotNullConstraint columnName=ALIAS, tableName=ORG; addUniqueConstraint constraintName=UK_ORG_ALIAS, tableName=ORG		\N	4.33.0	\N	\N	7560073650
26.0.0-org-group	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.065763	144	EXECUTED	9:da8e8087d80ef2ace4f89d8c5b9ca223	addColumn tableName=KEYCLOAK_GROUP; update tableName=KEYCLOAK_GROUP; addNotNullConstraint columnName=TYPE, tableName=KEYCLOAK_GROUP; customChange		\N	4.33.0	\N	\N	7560073650
26.0.0-org-indexes	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.079207	145	EXECUTED	9:79b05dcd610a8c7f25ec05135eec0857	createIndex indexName=IDX_ORG_DOMAIN_ORG_ID, tableName=ORG_DOMAIN		\N	4.33.0	\N	\N	7560073650
26.0.0-org-group-membership	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.080819	146	EXECUTED	9:a6ace2ce583a421d89b01ba2a28dc2d4	addColumn tableName=USER_GROUP_MEMBERSHIP; update tableName=USER_GROUP_MEMBERSHIP; addNotNullConstraint columnName=MEMBERSHIP_TYPE, tableName=USER_GROUP_MEMBERSHIP		\N	4.33.0	\N	\N	7560073650
31296-persist-revoked-access-tokens	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.082934	147	EXECUTED	9:64ef94489d42a358e8304b0e245f0ed4	createTable tableName=REVOKED_TOKEN; addPrimaryKey constraintName=CONSTRAINT_RT, tableName=REVOKED_TOKEN		\N	4.33.0	\N	\N	7560073650
31725-index-persist-revoked-access-tokens	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.095754	148	EXECUTED	9:b994246ec2bf7c94da881e1d28782c7b	createIndex indexName=IDX_REV_TOKEN_ON_EXPIRE, tableName=REVOKED_TOKEN		\N	4.33.0	\N	\N	7560073650
26.0.0-idps-for-login	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.140596	149	EXECUTED	9:51f5fffadf986983d4bd59582c6c1604	addColumn tableName=IDENTITY_PROVIDER; createIndex indexName=IDX_IDP_REALM_ORG, tableName=IDENTITY_PROVIDER; createIndex indexName=IDX_IDP_FOR_LOGIN, tableName=IDENTITY_PROVIDER; customChange		\N	4.33.0	\N	\N	7560073650
26.0.0-32583-drop-redundant-index-on-client-session	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.144139	150	EXECUTED	9:24972d83bf27317a055d234187bb4af9	dropIndex indexName=IDX_US_SESS_ID_ON_CL_SESS, tableName=OFFLINE_CLIENT_SESSION		\N	4.33.0	\N	\N	7560073650
26.0.0.32582-remove-tables-user-session-user-session-note-and-client-session	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.148453	151	EXECUTED	9:febdc0f47f2ed241c59e60f58c3ceea5	dropTable tableName=CLIENT_SESSION_ROLE; dropTable tableName=CLIENT_SESSION_NOTE; dropTable tableName=CLIENT_SESSION_PROT_MAPPER; dropTable tableName=CLIENT_SESSION_AUTH_STATUS; dropTable tableName=CLIENT_USER_SESSION_NOTE; dropTable tableName=CLI...		\N	4.33.0	\N	\N	7560073650
26.0.0-33201-org-redirect-url	keycloak	META-INF/jpa-changelog-26.0.0.xml	2026-04-30 14:41:18.149502	152	EXECUTED	9:4d0e22b0ac68ebe9794fa9cb752ea660	addColumn tableName=ORG		\N	4.33.0	\N	\N	7560073650
29399-jdbc-ping-default	keycloak	META-INF/jpa-changelog-26.1.0.xml	2026-04-30 14:41:18.152462	153	EXECUTED	9:007dbe99d7203fca403b89d4edfdf21e	createTable tableName=JGROUPS_PING; addPrimaryKey constraintName=CONSTRAINT_JGROUPS_PING, tableName=JGROUPS_PING		\N	4.33.0	\N	\N	7560073650
26.1.0-34013	keycloak	META-INF/jpa-changelog-26.1.0.xml	2026-04-30 14:41:18.154162	154	EXECUTED	9:e6b686a15759aef99a6d758a5c4c6a26	addColumn tableName=ADMIN_EVENT_ENTITY		\N	4.33.0	\N	\N	7560073650
26.1.0-34380	keycloak	META-INF/jpa-changelog-26.1.0.xml	2026-04-30 14:41:18.155555	155	EXECUTED	9:ac8b9edb7c2b6c17a1c7a11fcf5ccf01	dropTable tableName=USERNAME_LOGIN_FAILURE		\N	4.33.0	\N	\N	7560073650
26.2.0-36750	keycloak	META-INF/jpa-changelog-26.2.0.xml	2026-04-30 14:41:18.158508	156	EXECUTED	9:b49ce951c22f7eb16480ff085640a33a	createTable tableName=SERVER_CONFIG		\N	4.33.0	\N	\N	7560073650
26.2.0-26106	keycloak	META-INF/jpa-changelog-26.2.0.xml	2026-04-30 14:41:18.159613	157	EXECUTED	9:b5877d5dab7d10ff3a9d209d7beb6680	addColumn tableName=CREDENTIAL		\N	4.33.0	\N	\N	7560073650
26.2.6-39866-duplicate	keycloak	META-INF/jpa-changelog-26.2.6.xml	2026-04-30 14:41:18.160905	158	EXECUTED	9:1dc67ccee24f30331db2cba4f372e40e	customChange		\N	4.33.0	\N	\N	7560073650
26.2.6-39866-uk	keycloak	META-INF/jpa-changelog-26.2.6.xml	2026-04-30 14:41:18.162346	159	EXECUTED	9:b70b76f47210cf0a5f4ef0e219eac7cd	addUniqueConstraint constraintName=UK_MIGRATION_VERSION, tableName=MIGRATION_MODEL		\N	4.33.0	\N	\N	7560073650
26.2.6-40088-duplicate	keycloak	META-INF/jpa-changelog-26.2.6.xml	2026-04-30 14:41:18.163313	160	EXECUTED	9:cc7e02ed69ab31979afb1982f9670e8f	customChange		\N	4.33.0	\N	\N	7560073650
26.2.6-40088-uk	keycloak	META-INF/jpa-changelog-26.2.6.xml	2026-04-30 14:41:18.165924	161	EXECUTED	9:5bb848128da7bc4595cc507383325241	addUniqueConstraint constraintName=UK_MIGRATION_UPDATE_TIME, tableName=MIGRATION_MODEL		\N	4.33.0	\N	\N	7560073650
26.3.0-groups-description	keycloak	META-INF/jpa-changelog-26.3.0.xml	2026-04-30 14:41:18.167453	162	EXECUTED	9:e1a3c05574326fb5b246b73b9a4c4d49	addColumn tableName=KEYCLOAK_GROUP		\N	4.33.0	\N	\N	7560073650
26.4.0-40933-saml-encryption-attributes	keycloak	META-INF/jpa-changelog-26.4.0.xml	2026-04-30 14:41:18.168616	163	EXECUTED	9:7e9eaba362ca105efdda202303a4fe49	customChange		\N	4.33.0	\N	\N	7560073650
26.4.0-51321	keycloak	META-INF/jpa-changelog-26.4.0.xml	2026-04-30 14:41:18.183623	164	EXECUTED	9:34bab2bc56f75ffd7e347c580874e306	createIndex indexName=IDX_EVENT_ENTITY_USER_ID_TYPE, tableName=EVENT_ENTITY		\N	4.33.0	\N	\N	7560073650
40343-workflow-state-table	keycloak	META-INF/jpa-changelog-26.4.0.xml	2026-04-30 14:41:18.21373	165	EXECUTED	9:ed3ab4723ceed210e5b5e60ac4562106	createTable tableName=WORKFLOW_STATE; addPrimaryKey constraintName=PK_WORKFLOW_STATE, tableName=WORKFLOW_STATE; addUniqueConstraint constraintName=UQ_WORKFLOW_RESOURCE, tableName=WORKFLOW_STATE; createIndex indexName=IDX_WORKFLOW_STATE_STEP, table...		\N	4.33.0	\N	\N	7560073650
26.5.0-index-offline-css-by-client	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.295918	166	EXECUTED	9:383e981ce95d16e32af757b7998820f7	createIndex indexName=IDX_OFFLINE_CSS_BY_CLIENT, tableName=OFFLINE_CLIENT_SESSION		\N	4.33.0	\N	\N	7560073650
26.5.0-index-offline-css-by-client-storage-provider	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.318653	167	EXECUTED	9:f5bc200e6fa7d7e483854dee535ca425	createIndex indexName=IDX_OFFLINE_CSS_BY_CLIENT_STORAGE_PROVIDER, tableName=OFFLINE_CLIENT_SESSION		\N	4.33.0	\N	\N	7560073650
26.5.0-idp-config-allow-null	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.321871	168	EXECUTED	9:b667fb087874303b324c1af7fae4f606	dropDefaultValue columnName=TRUST_EMAIL, tableName=IDENTITY_PROVIDER; dropNotNullConstraint columnName=TRUST_EMAIL, tableName=IDENTITY_PROVIDER; dropNotNullConstraint columnName=STORE_TOKEN, tableName=IDENTITY_PROVIDER; dropDefaultValue columnName...		\N	4.33.0	\N	\N	7560073650
26.5.0-remove-workflow-provider-id-column	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.340815	169	EXECUTED	9:d8eeb324484d45e946d03b953e168b21	dropIndex indexName=IDX_WORKFLOW_STATE_PROVIDER, tableName=WORKFLOW_STATE; createIndex indexName=IDX_WORKFLOW_STATE_PROVIDER, tableName=WORKFLOW_STATE; dropColumn columnName=WORKFLOW_PROVIDER_ID, tableName=WORKFLOW_STATE		\N	4.33.0	\N	\N	7560073650
26.5.0-add-remember-me	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.34268	170	EXECUTED	9:a7273ea8b21bd2f674c9c49141999f05	addColumn tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
26.5.0-add-sess-refresh-idx	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.359523	171	EXECUTED	9:ce49383d317ccbcd3434d1f21172b0b7	createIndex indexName=IDX_USER_SESSION_EXPIRATION_CREATED, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
26.5.0-add-sess-create-idx	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.37728	172	EXECUTED	9:aaee09e23a4d8468fbc5c51b7b314c58	createIndex indexName=IDX_USER_SESSION_EXPIRATION_LAST_REFRESH, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
26.5.0-drop-sess-refresh-idx	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.379727	173	EXECUTED	9:f0082210b6ccbbaf81287c27aa23753c	dropIndex indexName=IDX_OFFLINE_USS_BY_LAST_SESSION_REFRESH, tableName=OFFLINE_USER_SESSION		\N	4.33.0	\N	\N	7560073650
26.5.0-invitations-table	keycloak	META-INF/jpa-changelog-26.5.0.xml	2026-04-30 14:41:18.428126	174	EXECUTED	9:322cb11fc03181903dcd67a54f8b3cf0	createTable tableName=ORG_INVITATION; addForeignKeyConstraint baseTableName=ORG_INVITATION, constraintName=FK_ORG_INVITATION_ORG, referencedTableName=ORG; createIndex indexName=IDX_ORG_INVITATION_ORG_ID, tableName=ORG_INVITATION; createIndex index...		\N	4.33.0	\N	\N	7560073650
\.


--
-- Data for Name: databasechangeloglock; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.databasechangeloglock (id, locked, lockgranted, lockedby) FROM stdin;
1	f	\N	\N
1000	f	\N	\N
\.


--
-- Data for Name: default_client_scope; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.default_client_scope (realm_id, scope_id, default_scope) FROM stdin;
950f7f4b-1af6-4a64-bb5e-2561faa87127	58912aa2-9f91-44c0-9d96-e9712da49547	f
950f7f4b-1af6-4a64-bb5e-2561faa87127	deb190e9-b3f3-4987-b52e-b2ce1268583f	t
950f7f4b-1af6-4a64-bb5e-2561faa87127	a097f9f9-5c79-4eba-af18-3cb6decdbb85	t
950f7f4b-1af6-4a64-bb5e-2561faa87127	ca6c61aa-bede-45fd-a52e-a4a548fb7068	t
950f7f4b-1af6-4a64-bb5e-2561faa87127	f09ae408-44af-4145-9086-0acc4d9b4011	t
950f7f4b-1af6-4a64-bb5e-2561faa87127	49bc6ebb-b477-4cc4-bd82-640d26338406	f
950f7f4b-1af6-4a64-bb5e-2561faa87127	43e08f49-41f4-4130-bf7e-2e35a36b717c	f
950f7f4b-1af6-4a64-bb5e-2561faa87127	4122c099-936e-4fcf-b236-1fda2083964b	t
950f7f4b-1af6-4a64-bb5e-2561faa87127	22117671-8539-42ba-8f4e-3c9422720fab	t
950f7f4b-1af6-4a64-bb5e-2561faa87127	a3f1a812-5c5a-43d4-8ba5-08bba228eb17	f
950f7f4b-1af6-4a64-bb5e-2561faa87127	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba	t
950f7f4b-1af6-4a64-bb5e-2561faa87127	09399803-e66a-4dd8-ab13-23b721d1a2e9	t
950f7f4b-1af6-4a64-bb5e-2561faa87127	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3	f
c55a12d3-a06b-43f4-b990-28390a55a7af	37506bdf-0373-4b65-81f0-97fcd9c8a32f	t
c55a12d3-a06b-43f4-b990-28390a55a7af	430e79f6-80c8-4bc6-bc8d-b9fad89705c2	t
c55a12d3-a06b-43f4-b990-28390a55a7af	ebc0e19e-d261-4423-b459-4f520f552fd8	t
c55a12d3-a06b-43f4-b990-28390a55a7af	1f1b437f-5f85-4c68-9bfa-9d82130c5f08	t
c55a12d3-a06b-43f4-b990-28390a55a7af	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c	t
c55a12d3-a06b-43f4-b990-28390a55a7af	ccae089a-7026-46a2-941d-cd676ef19750	t
c55a12d3-a06b-43f4-b990-28390a55a7af	4bef3907-f963-4ce5-b727-a3b95e0c1e36	t
c55a12d3-a06b-43f4-b990-28390a55a7af	d6e2a201-ae36-4402-981d-cd78cd93b451	t
c55a12d3-a06b-43f4-b990-28390a55a7af	11b465e1-9968-493c-b42c-ac582a714f76	f
c55a12d3-a06b-43f4-b990-28390a55a7af	909551aa-cac1-4add-8051-eff0829dee3e	f
c55a12d3-a06b-43f4-b990-28390a55a7af	74994a75-496d-432f-88d9-dabb47c922b5	f
c55a12d3-a06b-43f4-b990-28390a55a7af	045de1b1-5274-4d89-870d-ff589f80c2ff	f
c55a12d3-a06b-43f4-b990-28390a55a7af	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048	f
\.


--
-- Data for Name: event_entity; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.event_entity (id, client_id, details_json, error, ip_address, realm_id, session_id, event_time, type, user_id, details_json_long_value) FROM stdin;
\.


--
-- Data for Name: fed_user_attribute; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.fed_user_attribute (id, name, user_id, realm_id, storage_provider_id, value, long_value_hash, long_value_hash_lower_case, long_value) FROM stdin;
\.


--
-- Data for Name: fed_user_consent; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.fed_user_consent (id, client_id, user_id, realm_id, storage_provider_id, created_date, last_updated_date, client_storage_provider, external_client_id) FROM stdin;
\.


--
-- Data for Name: fed_user_consent_cl_scope; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.fed_user_consent_cl_scope (user_consent_id, scope_id) FROM stdin;
\.


--
-- Data for Name: fed_user_credential; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.fed_user_credential (id, salt, type, created_date, user_id, realm_id, storage_provider_id, user_label, secret_data, credential_data, priority) FROM stdin;
\.


--
-- Data for Name: fed_user_group_membership; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.fed_user_group_membership (group_id, user_id, realm_id, storage_provider_id) FROM stdin;
\.


--
-- Data for Name: fed_user_required_action; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.fed_user_required_action (required_action, user_id, realm_id, storage_provider_id) FROM stdin;
\.


--
-- Data for Name: fed_user_role_mapping; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.fed_user_role_mapping (role_id, user_id, realm_id, storage_provider_id) FROM stdin;
\.


--
-- Data for Name: federated_identity; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.federated_identity (identity_provider, realm_id, federated_user_id, federated_username, token, user_id) FROM stdin;
\.


--
-- Data for Name: federated_user; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.federated_user (id, storage_provider_id, realm_id) FROM stdin;
\.


--
-- Data for Name: group_attribute; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.group_attribute (id, name, value, group_id) FROM stdin;
\.


--
-- Data for Name: group_role_mapping; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.group_role_mapping (role_id, group_id) FROM stdin;
\.


--
-- Data for Name: identity_provider; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.identity_provider (internal_id, enabled, provider_alias, provider_id, store_token, authenticate_by_default, realm_id, add_token_role, trust_email, first_broker_login_flow_id, post_broker_login_flow_id, provider_display_name, link_only, organization_id, hide_on_login) FROM stdin;
\.


--
-- Data for Name: identity_provider_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.identity_provider_config (identity_provider_id, value, name) FROM stdin;
\.


--
-- Data for Name: identity_provider_mapper; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.identity_provider_mapper (id, name, idp_alias, idp_mapper_name, realm_id) FROM stdin;
\.


--
-- Data for Name: idp_mapper_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.idp_mapper_config (idp_mapper_id, value, name) FROM stdin;
\.


--
-- Data for Name: jgroups_ping; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.jgroups_ping (address, name, cluster_name, ip, coord) FROM stdin;
\.


--
-- Data for Name: keycloak_group; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.keycloak_group (id, name, parent_group, realm_id, type, description) FROM stdin;
\.


--
-- Data for Name: keycloak_role; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.keycloak_role (id, client_realm_constraint, client_role, description, name, realm_id, client, realm) FROM stdin;
33aa8679-f89d-47ee-8e63-d57d79270440	950f7f4b-1af6-4a64-bb5e-2561faa87127	f	${role_default-roles}	default-roles-master	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N	\N
36c982d0-3c1d-4472-95f5-63f2f2554ee6	950f7f4b-1af6-4a64-bb5e-2561faa87127	f	${role_admin}	admin	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N	\N
394521e0-fc27-4a81-b07b-3f2a5808a5cd	950f7f4b-1af6-4a64-bb5e-2561faa87127	f	${role_create-realm}	create-realm	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N	\N
3ca274e2-91d5-4cbc-82fe-c92630376a1f	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_create-client}	create-client	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
58858844-d6fa-4904-8ec8-ef3ddc817110	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_view-realm}	view-realm	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
c5b9c122-60d0-4b81-8cbd-ebd68bf8bece	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_view-users}	view-users	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
2a9eba64-cdd8-44aa-8bb4-3f372816a70b	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_view-clients}	view-clients	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
8476b2b7-1806-41c9-8b2c-70f957866126	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_view-events}	view-events	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
aa4626bb-7346-44cf-90e8-44d8ca5a2772	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_view-identity-providers}	view-identity-providers	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
ddb10a95-e481-43eb-bcf5-23356332f21c	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_view-authorization}	view-authorization	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
27be0898-95e0-4fed-9940-3724e1341040	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_manage-realm}	manage-realm	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
cf0edf92-25a5-402f-9860-784f35447df0	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_manage-users}	manage-users	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
17a019fe-a432-4319-b37c-ba2defd12b8d	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_manage-clients}	manage-clients	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
3a1c7506-233c-4db5-871f-8a08e1d8513a	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_manage-events}	manage-events	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
123a58a1-0ecd-42df-a7f8-ed74d8db0018	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_manage-identity-providers}	manage-identity-providers	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
eceb69d0-611e-4c2f-a343-65ea0e86409d	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_manage-authorization}	manage-authorization	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
fca1df51-7265-4d82-b1d6-5a89286333cc	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_query-users}	query-users	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
8edba74f-7ecd-449d-ba1b-5a111d6a23bb	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_query-clients}	query-clients	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
fa9bfdbf-65e4-4e16-b832-df366d709ce7	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_query-realms}	query-realms	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
36824ed7-29e3-4317-aba7-2d2c2c00ae1e	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_query-groups}	query-groups	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
caaf1f68-c0dc-483e-97c0-3738c9f80e96	70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	${role_view-profile}	view-profile	950f7f4b-1af6-4a64-bb5e-2561faa87127	70f8e924-f945-4a2a-b7f2-130505a5f8f7	\N
27737e8a-5ec2-4c3f-b929-725240133d56	70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	${role_manage-account}	manage-account	950f7f4b-1af6-4a64-bb5e-2561faa87127	70f8e924-f945-4a2a-b7f2-130505a5f8f7	\N
a36ba95a-8b4d-4fb6-b23f-aa7104a9bc11	70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	${role_manage-account-links}	manage-account-links	950f7f4b-1af6-4a64-bb5e-2561faa87127	70f8e924-f945-4a2a-b7f2-130505a5f8f7	\N
bb796d45-6361-4d8a-8c0d-0b2251db380f	70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	${role_view-applications}	view-applications	950f7f4b-1af6-4a64-bb5e-2561faa87127	70f8e924-f945-4a2a-b7f2-130505a5f8f7	\N
c3234aab-13b5-496e-b713-dd22c6d5b4f8	70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	${role_view-consent}	view-consent	950f7f4b-1af6-4a64-bb5e-2561faa87127	70f8e924-f945-4a2a-b7f2-130505a5f8f7	\N
78f5e097-8089-44c1-9803-c64ced351801	70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	${role_manage-consent}	manage-consent	950f7f4b-1af6-4a64-bb5e-2561faa87127	70f8e924-f945-4a2a-b7f2-130505a5f8f7	\N
b7b08417-b998-4183-8c77-7122fbc93c8a	70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	${role_view-groups}	view-groups	950f7f4b-1af6-4a64-bb5e-2561faa87127	70f8e924-f945-4a2a-b7f2-130505a5f8f7	\N
9f56a301-8568-4f92-84ac-c014d5d0a193	70f8e924-f945-4a2a-b7f2-130505a5f8f7	t	${role_delete-account}	delete-account	950f7f4b-1af6-4a64-bb5e-2561faa87127	70f8e924-f945-4a2a-b7f2-130505a5f8f7	\N
a705e3c1-21bc-4ef1-8178-cb5961b47d0b	4af7bbb0-5dbf-4fdd-b730-79b146a12050	t	${role_read-token}	read-token	950f7f4b-1af6-4a64-bb5e-2561faa87127	4af7bbb0-5dbf-4fdd-b730-79b146a12050	\N
af154f0c-e12a-4781-9b7b-e64914231226	a8ce899c-8a3d-4391-98dc-72610c85b515	t	${role_impersonation}	impersonation	950f7f4b-1af6-4a64-bb5e-2561faa87127	a8ce899c-8a3d-4391-98dc-72610c85b515	\N
c5c2e4d7-4e88-4aa8-981c-4984a37ec40b	950f7f4b-1af6-4a64-bb5e-2561faa87127	f	${role_offline-access}	offline_access	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N	\N
9811a0e5-94b6-44f0-a1aa-11194fa0a1d2	950f7f4b-1af6-4a64-bb5e-2561faa87127	f	${role_uma_authorization}	uma_authorization	950f7f4b-1af6-4a64-bb5e-2561faa87127	\N	\N
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	c55a12d3-a06b-43f4-b990-28390a55a7af	f	${role_default-roles}	default-roles-csfeer	c55a12d3-a06b-43f4-b990-28390a55a7af	\N	\N
bbfabec0-6afa-4ec8-8bcf-7eed2a200d02	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_create-client}	create-client	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
471a5e1a-d25f-48dc-93b5-9f3dd6042930	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_view-realm}	view-realm	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
ac625149-41cf-44a7-a4bc-09c81ed588ff	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_view-users}	view-users	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
6e3b3ebf-20b8-4efe-88c6-be13a5f5d262	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_view-clients}	view-clients	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
095c923a-1055-4e1f-8b23-936fd7caa3ff	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_view-events}	view-events	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
b6d208f9-790f-4d10-9c12-3d3eb9c444c7	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_view-identity-providers}	view-identity-providers	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
6c41cc69-db9d-49b3-80ab-6739d6ef06f2	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_view-authorization}	view-authorization	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
17a1ebfd-6234-46b1-bab8-9314c7c51a43	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_manage-realm}	manage-realm	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
8892692e-fdbc-4f52-991f-e6ca815ec4fa	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_manage-users}	manage-users	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
778554df-db55-4ff0-ad3f-97ae274f0f96	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_manage-clients}	manage-clients	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
dc8f3e18-5aa3-406c-8ab2-2395b608de1c	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_manage-events}	manage-events	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
c9f1e0e0-1d39-48bf-9e41-78e01c5b7e03	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_manage-identity-providers}	manage-identity-providers	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
46b2f33a-b7ee-4021-922e-b7c2da4da216	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_manage-authorization}	manage-authorization	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
3d19a544-2c7b-4ce9-8f0b-061d66a3afc8	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_query-users}	query-users	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
62871172-bca6-4bd9-bf2c-1a07a4f9fcae	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_query-clients}	query-clients	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
e4de23f9-d355-400f-89ce-bd1d2d75236b	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_query-realms}	query-realms	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
e691f5aa-11ef-4230-b6d5-4d5b25abdd5e	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_query-groups}	query-groups	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
abd702be-194e-420f-9a46-821e6340a8dd	c55a12d3-a06b-43f4-b990-28390a55a7af	f	${role_offline-access}	offline_access	c55a12d3-a06b-43f4-b990-28390a55a7af	\N	\N
ffc312c1-b2ef-49e3-97bd-3b56b6102ded	c55a12d3-a06b-43f4-b990-28390a55a7af	f	${role_uma_authorization}	uma_authorization	c55a12d3-a06b-43f4-b990-28390a55a7af	\N	\N
a1b2c3d4-e5f6-4789-a012-3456789abcde	c55a12d3-a06b-43f4-b990-28390a55a7af	f	CSFEER Administrator Role	csfeer_admin	c55a12d3-a06b-43f4-b990-28390a55a7af	\N	\N
b2c3d4e5-f6a7-4890-b123-456789abcdef	c55a12d3-a06b-43f4-b990-28390a55a7af	f	CSFEER User Role	csfeer_user	c55a12d3-a06b-43f4-b990-28390a55a7af	\N	\N
bd2e3de6-6bc2-4f17-880b-9be4367ed89d	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_create-client}	create-client	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
f3f65afa-a38b-450e-a812-6e1f0b6b5f58	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_manage-events}	manage-events	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
cf817ac6-42b0-4494-9df0-3c6a9bbd2de7	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_manage-clients}	manage-clients	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
ee1d0b58-e578-4b1f-b189-5da60ed85f15	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_manage-identity-providers}	manage-identity-providers	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
de7e7a89-0e7d-4bea-aed5-93f32f824640	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_query-realms}	query-realms	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
e6ff11d6-a1c1-4c1b-8818-47c07f24d7dc	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_query-users}	query-users	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
ca35c48c-f30a-4c0a-89c7-adab1347c185	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_view-authorization}	view-authorization	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
0e78d5e6-550e-445f-bc61-21409b052e41	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_view-users}	view-users	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
01d5015d-222d-4445-906b-971bbe4df9c8	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_manage-authorization}	manage-authorization	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
81ba14ed-6f2c-4e24-abb1-ef97b6c87057	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_manage-users}	manage-users	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
24e9d6a5-f1a4-481e-b855-1cf6b92027b4	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_impersonation}	impersonation	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
92bd35f9-b02c-4ae0-b18f-f3f78c08d1f7	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_view-events}	view-events	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
826dabc6-e7fc-410f-bba4-90a29f234ba8	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_view-clients}	view-clients	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
057b70e0-e7ed-4e04-9c3f-2ef55a0c2748	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_realm-admin}	realm-admin	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
962f06a2-f97a-4c53-9793-be7f45360ed2	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_query-clients}	query-clients	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
b7cf881a-f662-4c05-90b9-8cce965cc72c	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_view-realm}	view-realm	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
6294e231-a2c7-40e6-95e6-bf7cce8b5570	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_manage-realm}	manage-realm	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
36b77f6f-bc11-4f40-9922-7ef323ec2691	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_query-groups}	query-groups	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
01a0f4a4-a6d1-4dce-afdf-fe14f65dcf65	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	t	${role_view-identity-providers}	view-identity-providers	c55a12d3-a06b-43f4-b990-28390a55a7af	1fe7b7e3-f751-4f73-b409-d6bfd5d8e600	\N
e6ee715f-74bd-43a6-84c1-7e7a265acae1	b141edca-aa19-47f5-87be-23de76c8a44f	t	${role_read-token}	read-token	c55a12d3-a06b-43f4-b990-28390a55a7af	b141edca-aa19-47f5-87be-23de76c8a44f	\N
890da050-44a1-4d3a-aa8a-3c6ad9d225d9	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	${role_manage-consent}	manage-consent	c55a12d3-a06b-43f4-b990-28390a55a7af	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	\N
1dec6fcb-0eec-473f-8a1c-e3c12ebcd73e	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	${role_manage-account}	manage-account	c55a12d3-a06b-43f4-b990-28390a55a7af	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	\N
bc8c26cd-60af-42bd-956d-b52022a8159a	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	${role_manage-account-links}	manage-account-links	c55a12d3-a06b-43f4-b990-28390a55a7af	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	\N
12c7f507-8082-46bf-9062-60ec79ff58d5	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	${role_view-applications}	view-applications	c55a12d3-a06b-43f4-b990-28390a55a7af	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	\N
3d831730-fb07-4e8e-8afb-1f6060f7beae	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	${role_view-groups}	view-groups	c55a12d3-a06b-43f4-b990-28390a55a7af	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	\N
9c7d0834-aa6a-45db-9524-65370194d514	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	${role_view-consent}	view-consent	c55a12d3-a06b-43f4-b990-28390a55a7af	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	\N
fc77baf5-cf87-49ff-9915-7583c284d482	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	${role_view-profile}	view-profile	c55a12d3-a06b-43f4-b990-28390a55a7af	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	\N
6acc6eda-6b5b-4b09-8673-f355f9318d2d	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	t	${role_delete-account}	delete-account	c55a12d3-a06b-43f4-b990-28390a55a7af	3a97fb4a-6f6e-4174-bcf3-d80116bb5036	\N
0aef58e9-e808-4809-a53d-d1ae5c8331ec	ce82e997-d439-4acf-8d80-8c0ed9b401b4	t	${role_impersonation}	impersonation	950f7f4b-1af6-4a64-bb5e-2561faa87127	ce82e997-d439-4acf-8d80-8c0ed9b401b4	\N
\.


--
-- Data for Name: migration_model; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.migration_model (id, version, update_time) FROM stdin;
gxh6l	26.5.0	1777560079
\.


--
-- Data for Name: offline_client_session; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.offline_client_session (user_session_id, client_id, offline_flag, "timestamp", data, client_storage_provider, external_client_id, version) FROM stdin;
A9ez_b2aaPd3vcdsqdWKpK4i	b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e	0	1777560082	{"authMethod":"openid-connect","notes":{"clientId":"b3ff3419-c7f2-4c8e-9312-2b32ee6eec5e","userSessionStartedAt":"1777560082","iss":"http://oauth.csfeer:8081/realms/master","startedAt":"1777560082","level-of-authentication":"-1"}}	local	local	0
\.


--
-- Data for Name: offline_user_session; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.offline_user_session (user_session_id, user_id, realm_id, created_on, offline_flag, data, last_session_refresh, broker_session_id, version, remember_me) FROM stdin;
A9ez_b2aaPd3vcdsqdWKpK4i	dad2c622-f878-4d62-8ae2-39bfe52003ae	950f7f4b-1af6-4a64-bb5e-2561faa87127	1777560082	0	{"ipAddress":"172.20.0.4","authMethod":"openid-connect","rememberMe":false,"started":0,"notes":{"KC_DEVICE_NOTE":"eyJpcEFkZHJlc3MiOiIxNzIuMjAuMC40Iiwib3MiOiJPdGhlciIsIm9zVmVyc2lvbiI6IlVua25vd24iLCJicm93c2VyIjoiQXBhY2hlLUh0dHBDbGllbnQvNC41LjE0IiwiZGV2aWNlIjoiT3RoZXIiLCJsYXN0QWNjZXNzIjowLCJtb2JpbGUiOmZhbHNlfQ==","authenticators-completed":"{\\"e59360aa-4a60-4191-ad48-05df1d0628eb\\":1777560082,\\"931230be-dfc7-4eb2-b069-535e7b320932\\":1777560082}"},"state":"LOGGED_IN"}	1777560082	\N	0	f
\.


--
-- Data for Name: org; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.org (id, enabled, realm_id, group_id, name, description, alias, redirect_url) FROM stdin;
\.


--
-- Data for Name: org_domain; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.org_domain (id, name, verified, org_id) FROM stdin;
\.


--
-- Data for Name: org_invitation; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.org_invitation (id, organization_id, email, first_name, last_name, created_at, expires_at, invite_link) FROM stdin;
\.


--
-- Data for Name: policy_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.policy_config (policy_id, name, value) FROM stdin;
\.


--
-- Data for Name: protocol_mapper; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.protocol_mapper (id, name, protocol, protocol_mapper_name, client_id, client_scope_id) FROM stdin;
44da43f5-140a-46f5-99be-8eaeedeb54f8	audience resolve	openid-connect	oidc-audience-resolve-mapper	640d1fae-9a47-46dc-81d3-8ed39870984a	\N
d9c9e01e-d734-4a67-99ad-3ef1c9a7a5d1	locale	openid-connect	oidc-usermodel-attribute-mapper	1019acd8-53d9-4ee6-959a-9a5b4660bdc1	\N
f6a54aee-cad2-446f-8644-46a0ddf4732d	role list	saml	saml-role-list-mapper	\N	deb190e9-b3f3-4987-b52e-b2ce1268583f
35d4aa80-3baa-4eff-97ef-1535b1be3b9e	organization	saml	saml-organization-membership-mapper	\N	a097f9f9-5c79-4eba-af18-3cb6decdbb85
3e4dc01a-3ea0-49b0-aea4-f5666a7d968c	full name	openid-connect	oidc-full-name-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
a10a55e4-2379-439c-839a-6d47dc6de9b2	family name	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
49a79b24-fdf6-40bb-be3c-45f8bd1af7db	given name	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
771e7e65-9e18-4343-a217-422910c6f152	middle name	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
25a7adf7-ada0-423b-bda8-cf111a679b77	nickname	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
ccb2d886-1161-42f9-9a06-fbfca86295c1	username	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
9012a5e6-0644-4857-aa7d-e6b3441664f7	profile	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
8e846081-a9fc-4aa3-932c-3800a46bd833	picture	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
10d69646-12d3-4f66-9fd3-f5d8a67be1b4	website	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
70e376c3-39d6-4ba0-a1b8-4456769f4dfc	gender	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
aaef2d3a-1168-45d8-becf-6246e7e8bf87	birthdate	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
9d91c5a3-1a74-437b-9733-1f51b5002712	zoneinfo	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
8f00ae39-16d9-4d9b-b0d9-036f5e325cd4	locale	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
6744856b-d8e4-4264-8abe-a24e7e7ce636	updated at	openid-connect	oidc-usermodel-attribute-mapper	\N	ca6c61aa-bede-45fd-a52e-a4a548fb7068
df21b034-e7b5-4119-afe8-ac436a9ba12f	email	openid-connect	oidc-usermodel-attribute-mapper	\N	f09ae408-44af-4145-9086-0acc4d9b4011
5f093563-3810-4b70-a77c-55cadf2a0167	email verified	openid-connect	oidc-usermodel-property-mapper	\N	f09ae408-44af-4145-9086-0acc4d9b4011
0db47b0c-749c-4557-b697-c234c13e85ce	address	openid-connect	oidc-address-mapper	\N	49bc6ebb-b477-4cc4-bd82-640d26338406
925e0c75-919d-48be-bc5b-d3a97c67e085	phone number	openid-connect	oidc-usermodel-attribute-mapper	\N	43e08f49-41f4-4130-bf7e-2e35a36b717c
770c96d6-b580-489c-9dea-bfe7d06d3b0d	phone number verified	openid-connect	oidc-usermodel-attribute-mapper	\N	43e08f49-41f4-4130-bf7e-2e35a36b717c
a618d5ed-7e33-41d3-b2e5-fe745c92459d	realm roles	openid-connect	oidc-usermodel-realm-role-mapper	\N	4122c099-936e-4fcf-b236-1fda2083964b
87be9ec0-f3ed-4f8a-bd95-cf026b89834d	client roles	openid-connect	oidc-usermodel-client-role-mapper	\N	4122c099-936e-4fcf-b236-1fda2083964b
3aa346da-c923-44f2-bb85-b54d80a290ea	audience resolve	openid-connect	oidc-audience-resolve-mapper	\N	4122c099-936e-4fcf-b236-1fda2083964b
69a5dfc8-0f8a-4aa0-b7c6-73c1f790cf0d	allowed web origins	openid-connect	oidc-allowed-origins-mapper	\N	22117671-8539-42ba-8f4e-3c9422720fab
1f190fcf-57fd-4dba-8049-7aa8dd43a52a	upn	openid-connect	oidc-usermodel-attribute-mapper	\N	a3f1a812-5c5a-43d4-8ba5-08bba228eb17
18a190b8-6388-406e-bd22-a20236ee1c08	groups	openid-connect	oidc-usermodel-realm-role-mapper	\N	a3f1a812-5c5a-43d4-8ba5-08bba228eb17
47faf84b-184c-40f0-bdbd-da14352589ec	acr loa level	openid-connect	oidc-acr-mapper	\N	3a76aae4-7a7c-4a6b-a67a-6eb2cffb6bba
3e6d4d9b-eb0d-4c50-9fc0-700ffe944044	auth_time	openid-connect	oidc-usersessionmodel-note-mapper	\N	09399803-e66a-4dd8-ab13-23b721d1a2e9
11d799a0-56c1-454b-8451-b7052932e198	sub	openid-connect	oidc-sub-mapper	\N	09399803-e66a-4dd8-ab13-23b721d1a2e9
7314f796-8152-4194-b566-9ea48b84332b	Client ID	openid-connect	oidc-usersessionmodel-note-mapper	\N	48078758-f8c1-4b6c-bffe-93addc0eeeb5
3d947aa0-c00f-4e77-bd41-311968ca4dea	Client Host	openid-connect	oidc-usersessionmodel-note-mapper	\N	48078758-f8c1-4b6c-bffe-93addc0eeeb5
a2ac6e6b-d806-48cd-bde6-c52fa567b72f	Client IP Address	openid-connect	oidc-usersessionmodel-note-mapper	\N	48078758-f8c1-4b6c-bffe-93addc0eeeb5
7f874995-f57c-42fd-a1b2-fadfe09239e7	organization	openid-connect	oidc-organization-membership-mapper	\N	b163b8e2-a8ba-48c8-9dc6-fb310da1e7e3
f7ac5b9c-5dfd-4c92-b43d-e6d93615fa0a	organization	openid-connect	oidc-organization-membership-mapper	\N	c5fdbda6-ce2b-4fdb-97bf-ab2ace21e048
fe2c000d-31ce-4376-aea6-f623e185768f	role list	saml	saml-role-list-mapper	\N	37506bdf-0373-4b65-81f0-97fcd9c8a32f
c9c5128a-45b7-4154-9d6b-4ac92baa9789	allowed web origins	openid-connect	oidc-allowed-origins-mapper	\N	ccae089a-7026-46a2-941d-cd676ef19750
174ea913-404e-4cd5-8aa2-e52de3e3f66c	client roles	openid-connect	oidc-usermodel-client-role-mapper	\N	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c
640a3ec0-d2ab-447d-9e74-92648c6351ea	realm roles	openid-connect	oidc-usermodel-realm-role-mapper	\N	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c
bbd7e124-5e2e-47c8-9713-3b810ad627f9	audience resolve	openid-connect	oidc-audience-resolve-mapper	\N	153d6afc-8bd5-4b9b-b08e-21c9ca3cae7c
50496409-83c7-43cf-8055-44530f93c54e	groups	openid-connect	oidc-usermodel-realm-role-mapper	\N	045de1b1-5274-4d89-870d-ff589f80c2ff
2cd8120e-4141-42d8-948f-fde701030d00	upn	openid-connect	oidc-usermodel-attribute-mapper	\N	045de1b1-5274-4d89-870d-ff589f80c2ff
45056b20-b279-4c53-8843-52c068ada784	sub	openid-connect	oidc-sub-mapper	\N	d6e2a201-ae36-4402-981d-cd78cd93b451
5ffaf19f-fc3b-472d-ba4f-b70578b86f93	auth_time	openid-connect	oidc-usersessionmodel-note-mapper	\N	d6e2a201-ae36-4402-981d-cd78cd93b451
292b26b9-3570-44c2-90ab-789370a6bfde	full name	openid-connect	oidc-full-name-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
e578983d-3343-4e07-b8be-58f52398777b	birthdate	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
5b4e2c0a-b29d-4a20-85bd-f05ac705ee32	zoneinfo	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
74135e06-87e9-45d2-b38f-99ca91554155	website	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
0d3926a8-e081-4f08-ba70-ac3f3b4f5d1f	nickname	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
c75a2060-d8c9-483c-83a1-316e36b968eb	family name	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
ce4a8627-24e7-4831-afa4-cdb1ad897637	middle name	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
6dffadc9-89a7-4f79-8e1a-f75fdf7294a9	picture	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
34ae1958-66ca-4e5b-b704-a2685839834c	gender	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
221c166c-b7f6-4674-a0f9-fe5fa9e1c552	username	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
782dea23-dd14-4d84-8cc2-877ff02179d9	given name	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
c796224b-675e-4f85-92e0-911e2dd09338	profile	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
6e8b96ac-e04f-41d1-a341-bf093d5aeb7b	locale	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
cca39f77-72ea-4890-afb3-10f52018227e	updated at	openid-connect	oidc-usermodel-attribute-mapper	\N	ebc0e19e-d261-4423-b459-4f520f552fd8
ad75cd0a-717e-4329-b0d3-095d370d08aa	organization	saml	saml-organization-membership-mapper	\N	430e79f6-80c8-4bc6-bc8d-b9fad89705c2
a2d788f5-2b79-4268-a239-2708756f0675	phone number	openid-connect	oidc-usermodel-attribute-mapper	\N	74994a75-496d-432f-88d9-dabb47c922b5
c7528bc7-aeb8-4c4a-b38f-42b5b58adbc8	phone number verified	openid-connect	oidc-usermodel-attribute-mapper	\N	74994a75-496d-432f-88d9-dabb47c922b5
3588a16b-0d7c-4790-9c81-306b71a10d07	acr loa level	openid-connect	oidc-acr-mapper	\N	4bef3907-f963-4ce5-b727-a3b95e0c1e36
2138f335-c272-4415-8bec-584d84cabdbb	Client ID	openid-connect	oidc-usersessionmodel-note-mapper	\N	15bbb040-e553-4b52-9e80-47006803f558
59176ff1-9076-488a-a063-bf78600fa37f	Client Host	openid-connect	oidc-usersessionmodel-note-mapper	\N	15bbb040-e553-4b52-9e80-47006803f558
549f29c0-adc2-4695-ae1a-70ae30479837	Client IP Address	openid-connect	oidc-usersessionmodel-note-mapper	\N	15bbb040-e553-4b52-9e80-47006803f558
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	address	openid-connect	oidc-address-mapper	\N	909551aa-cac1-4add-8051-eff0829dee3e
dba5e1e9-96ff-468b-9c27-70665d8acd93	email	openid-connect	oidc-usermodel-attribute-mapper	\N	1f1b437f-5f85-4c68-9bfa-9d82130c5f08
a9cc5c7a-c2e8-44bd-b117-a521328ec607	email verified	openid-connect	oidc-usermodel-property-mapper	\N	1f1b437f-5f85-4c68-9bfa-9d82130c5f08
e18cb40b-6654-4279-ae0c-73aae98793b6	audience resolve	openid-connect	oidc-audience-resolve-mapper	c003a982-e593-4ee1-9a4c-02fd6c6b29fa	\N
73167c87-cee2-46e2-a5ca-57e85f395650	locale	openid-connect	oidc-usermodel-attribute-mapper	043917f3-a51e-4661-83c1-41b19f4ee3fe	\N
\.


--
-- Data for Name: protocol_mapper_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.protocol_mapper_config (protocol_mapper_id, value, name) FROM stdin;
d9c9e01e-d734-4a67-99ad-3ef1c9a7a5d1	true	introspection.token.claim
d9c9e01e-d734-4a67-99ad-3ef1c9a7a5d1	true	userinfo.token.claim
d9c9e01e-d734-4a67-99ad-3ef1c9a7a5d1	locale	user.attribute
d9c9e01e-d734-4a67-99ad-3ef1c9a7a5d1	true	id.token.claim
d9c9e01e-d734-4a67-99ad-3ef1c9a7a5d1	true	access.token.claim
d9c9e01e-d734-4a67-99ad-3ef1c9a7a5d1	locale	claim.name
d9c9e01e-d734-4a67-99ad-3ef1c9a7a5d1	String	jsonType.label
f6a54aee-cad2-446f-8644-46a0ddf4732d	false	single
f6a54aee-cad2-446f-8644-46a0ddf4732d	Basic	attribute.nameformat
f6a54aee-cad2-446f-8644-46a0ddf4732d	Role	attribute.name
10d69646-12d3-4f66-9fd3-f5d8a67be1b4	true	introspection.token.claim
10d69646-12d3-4f66-9fd3-f5d8a67be1b4	true	userinfo.token.claim
10d69646-12d3-4f66-9fd3-f5d8a67be1b4	website	user.attribute
10d69646-12d3-4f66-9fd3-f5d8a67be1b4	true	id.token.claim
10d69646-12d3-4f66-9fd3-f5d8a67be1b4	true	access.token.claim
10d69646-12d3-4f66-9fd3-f5d8a67be1b4	website	claim.name
10d69646-12d3-4f66-9fd3-f5d8a67be1b4	String	jsonType.label
25a7adf7-ada0-423b-bda8-cf111a679b77	true	introspection.token.claim
25a7adf7-ada0-423b-bda8-cf111a679b77	true	userinfo.token.claim
25a7adf7-ada0-423b-bda8-cf111a679b77	nickname	user.attribute
25a7adf7-ada0-423b-bda8-cf111a679b77	true	id.token.claim
25a7adf7-ada0-423b-bda8-cf111a679b77	true	access.token.claim
25a7adf7-ada0-423b-bda8-cf111a679b77	nickname	claim.name
25a7adf7-ada0-423b-bda8-cf111a679b77	String	jsonType.label
3e4dc01a-3ea0-49b0-aea4-f5666a7d968c	true	introspection.token.claim
3e4dc01a-3ea0-49b0-aea4-f5666a7d968c	true	userinfo.token.claim
3e4dc01a-3ea0-49b0-aea4-f5666a7d968c	true	id.token.claim
3e4dc01a-3ea0-49b0-aea4-f5666a7d968c	true	access.token.claim
49a79b24-fdf6-40bb-be3c-45f8bd1af7db	true	introspection.token.claim
49a79b24-fdf6-40bb-be3c-45f8bd1af7db	true	userinfo.token.claim
49a79b24-fdf6-40bb-be3c-45f8bd1af7db	firstName	user.attribute
49a79b24-fdf6-40bb-be3c-45f8bd1af7db	true	id.token.claim
49a79b24-fdf6-40bb-be3c-45f8bd1af7db	true	access.token.claim
49a79b24-fdf6-40bb-be3c-45f8bd1af7db	given_name	claim.name
49a79b24-fdf6-40bb-be3c-45f8bd1af7db	String	jsonType.label
6744856b-d8e4-4264-8abe-a24e7e7ce636	true	introspection.token.claim
6744856b-d8e4-4264-8abe-a24e7e7ce636	true	userinfo.token.claim
6744856b-d8e4-4264-8abe-a24e7e7ce636	updatedAt	user.attribute
6744856b-d8e4-4264-8abe-a24e7e7ce636	true	id.token.claim
6744856b-d8e4-4264-8abe-a24e7e7ce636	true	access.token.claim
6744856b-d8e4-4264-8abe-a24e7e7ce636	updated_at	claim.name
6744856b-d8e4-4264-8abe-a24e7e7ce636	long	jsonType.label
70e376c3-39d6-4ba0-a1b8-4456769f4dfc	true	introspection.token.claim
70e376c3-39d6-4ba0-a1b8-4456769f4dfc	true	userinfo.token.claim
70e376c3-39d6-4ba0-a1b8-4456769f4dfc	gender	user.attribute
70e376c3-39d6-4ba0-a1b8-4456769f4dfc	true	id.token.claim
70e376c3-39d6-4ba0-a1b8-4456769f4dfc	true	access.token.claim
70e376c3-39d6-4ba0-a1b8-4456769f4dfc	gender	claim.name
70e376c3-39d6-4ba0-a1b8-4456769f4dfc	String	jsonType.label
771e7e65-9e18-4343-a217-422910c6f152	true	introspection.token.claim
771e7e65-9e18-4343-a217-422910c6f152	true	userinfo.token.claim
771e7e65-9e18-4343-a217-422910c6f152	middleName	user.attribute
771e7e65-9e18-4343-a217-422910c6f152	true	id.token.claim
771e7e65-9e18-4343-a217-422910c6f152	true	access.token.claim
771e7e65-9e18-4343-a217-422910c6f152	middle_name	claim.name
771e7e65-9e18-4343-a217-422910c6f152	String	jsonType.label
8e846081-a9fc-4aa3-932c-3800a46bd833	true	introspection.token.claim
8e846081-a9fc-4aa3-932c-3800a46bd833	true	userinfo.token.claim
8e846081-a9fc-4aa3-932c-3800a46bd833	picture	user.attribute
8e846081-a9fc-4aa3-932c-3800a46bd833	true	id.token.claim
8e846081-a9fc-4aa3-932c-3800a46bd833	true	access.token.claim
8e846081-a9fc-4aa3-932c-3800a46bd833	picture	claim.name
8e846081-a9fc-4aa3-932c-3800a46bd833	String	jsonType.label
8f00ae39-16d9-4d9b-b0d9-036f5e325cd4	true	introspection.token.claim
8f00ae39-16d9-4d9b-b0d9-036f5e325cd4	true	userinfo.token.claim
8f00ae39-16d9-4d9b-b0d9-036f5e325cd4	locale	user.attribute
8f00ae39-16d9-4d9b-b0d9-036f5e325cd4	true	id.token.claim
8f00ae39-16d9-4d9b-b0d9-036f5e325cd4	true	access.token.claim
8f00ae39-16d9-4d9b-b0d9-036f5e325cd4	locale	claim.name
8f00ae39-16d9-4d9b-b0d9-036f5e325cd4	String	jsonType.label
9012a5e6-0644-4857-aa7d-e6b3441664f7	true	introspection.token.claim
9012a5e6-0644-4857-aa7d-e6b3441664f7	true	userinfo.token.claim
9012a5e6-0644-4857-aa7d-e6b3441664f7	profile	user.attribute
9012a5e6-0644-4857-aa7d-e6b3441664f7	true	id.token.claim
9012a5e6-0644-4857-aa7d-e6b3441664f7	true	access.token.claim
9012a5e6-0644-4857-aa7d-e6b3441664f7	profile	claim.name
9012a5e6-0644-4857-aa7d-e6b3441664f7	String	jsonType.label
9d91c5a3-1a74-437b-9733-1f51b5002712	true	introspection.token.claim
9d91c5a3-1a74-437b-9733-1f51b5002712	true	userinfo.token.claim
9d91c5a3-1a74-437b-9733-1f51b5002712	zoneinfo	user.attribute
9d91c5a3-1a74-437b-9733-1f51b5002712	true	id.token.claim
9d91c5a3-1a74-437b-9733-1f51b5002712	true	access.token.claim
9d91c5a3-1a74-437b-9733-1f51b5002712	zoneinfo	claim.name
9d91c5a3-1a74-437b-9733-1f51b5002712	String	jsonType.label
a10a55e4-2379-439c-839a-6d47dc6de9b2	true	introspection.token.claim
a10a55e4-2379-439c-839a-6d47dc6de9b2	true	userinfo.token.claim
a10a55e4-2379-439c-839a-6d47dc6de9b2	lastName	user.attribute
a10a55e4-2379-439c-839a-6d47dc6de9b2	true	id.token.claim
a10a55e4-2379-439c-839a-6d47dc6de9b2	true	access.token.claim
a10a55e4-2379-439c-839a-6d47dc6de9b2	family_name	claim.name
a10a55e4-2379-439c-839a-6d47dc6de9b2	String	jsonType.label
aaef2d3a-1168-45d8-becf-6246e7e8bf87	true	introspection.token.claim
aaef2d3a-1168-45d8-becf-6246e7e8bf87	true	userinfo.token.claim
aaef2d3a-1168-45d8-becf-6246e7e8bf87	birthdate	user.attribute
aaef2d3a-1168-45d8-becf-6246e7e8bf87	true	id.token.claim
aaef2d3a-1168-45d8-becf-6246e7e8bf87	true	access.token.claim
aaef2d3a-1168-45d8-becf-6246e7e8bf87	birthdate	claim.name
aaef2d3a-1168-45d8-becf-6246e7e8bf87	String	jsonType.label
ccb2d886-1161-42f9-9a06-fbfca86295c1	true	introspection.token.claim
ccb2d886-1161-42f9-9a06-fbfca86295c1	true	userinfo.token.claim
ccb2d886-1161-42f9-9a06-fbfca86295c1	username	user.attribute
ccb2d886-1161-42f9-9a06-fbfca86295c1	true	id.token.claim
ccb2d886-1161-42f9-9a06-fbfca86295c1	true	access.token.claim
ccb2d886-1161-42f9-9a06-fbfca86295c1	preferred_username	claim.name
ccb2d886-1161-42f9-9a06-fbfca86295c1	String	jsonType.label
5f093563-3810-4b70-a77c-55cadf2a0167	true	introspection.token.claim
5f093563-3810-4b70-a77c-55cadf2a0167	true	userinfo.token.claim
5f093563-3810-4b70-a77c-55cadf2a0167	emailVerified	user.attribute
5f093563-3810-4b70-a77c-55cadf2a0167	true	id.token.claim
5f093563-3810-4b70-a77c-55cadf2a0167	true	access.token.claim
5f093563-3810-4b70-a77c-55cadf2a0167	email_verified	claim.name
5f093563-3810-4b70-a77c-55cadf2a0167	boolean	jsonType.label
df21b034-e7b5-4119-afe8-ac436a9ba12f	true	introspection.token.claim
df21b034-e7b5-4119-afe8-ac436a9ba12f	true	userinfo.token.claim
df21b034-e7b5-4119-afe8-ac436a9ba12f	email	user.attribute
df21b034-e7b5-4119-afe8-ac436a9ba12f	true	id.token.claim
df21b034-e7b5-4119-afe8-ac436a9ba12f	true	access.token.claim
df21b034-e7b5-4119-afe8-ac436a9ba12f	email	claim.name
df21b034-e7b5-4119-afe8-ac436a9ba12f	String	jsonType.label
0db47b0c-749c-4557-b697-c234c13e85ce	formatted	user.attribute.formatted
0db47b0c-749c-4557-b697-c234c13e85ce	country	user.attribute.country
0db47b0c-749c-4557-b697-c234c13e85ce	true	introspection.token.claim
0db47b0c-749c-4557-b697-c234c13e85ce	postal_code	user.attribute.postal_code
0db47b0c-749c-4557-b697-c234c13e85ce	true	userinfo.token.claim
0db47b0c-749c-4557-b697-c234c13e85ce	street	user.attribute.street
0db47b0c-749c-4557-b697-c234c13e85ce	true	id.token.claim
0db47b0c-749c-4557-b697-c234c13e85ce	region	user.attribute.region
0db47b0c-749c-4557-b697-c234c13e85ce	true	access.token.claim
0db47b0c-749c-4557-b697-c234c13e85ce	locality	user.attribute.locality
770c96d6-b580-489c-9dea-bfe7d06d3b0d	true	introspection.token.claim
770c96d6-b580-489c-9dea-bfe7d06d3b0d	true	userinfo.token.claim
770c96d6-b580-489c-9dea-bfe7d06d3b0d	phoneNumberVerified	user.attribute
770c96d6-b580-489c-9dea-bfe7d06d3b0d	true	id.token.claim
770c96d6-b580-489c-9dea-bfe7d06d3b0d	true	access.token.claim
770c96d6-b580-489c-9dea-bfe7d06d3b0d	phone_number_verified	claim.name
770c96d6-b580-489c-9dea-bfe7d06d3b0d	boolean	jsonType.label
925e0c75-919d-48be-bc5b-d3a97c67e085	true	introspection.token.claim
925e0c75-919d-48be-bc5b-d3a97c67e085	true	userinfo.token.claim
925e0c75-919d-48be-bc5b-d3a97c67e085	phoneNumber	user.attribute
925e0c75-919d-48be-bc5b-d3a97c67e085	true	id.token.claim
925e0c75-919d-48be-bc5b-d3a97c67e085	true	access.token.claim
925e0c75-919d-48be-bc5b-d3a97c67e085	phone_number	claim.name
925e0c75-919d-48be-bc5b-d3a97c67e085	String	jsonType.label
3aa346da-c923-44f2-bb85-b54d80a290ea	true	introspection.token.claim
3aa346da-c923-44f2-bb85-b54d80a290ea	true	access.token.claim
87be9ec0-f3ed-4f8a-bd95-cf026b89834d	true	introspection.token.claim
87be9ec0-f3ed-4f8a-bd95-cf026b89834d	true	multivalued
87be9ec0-f3ed-4f8a-bd95-cf026b89834d	foo	user.attribute
87be9ec0-f3ed-4f8a-bd95-cf026b89834d	true	access.token.claim
87be9ec0-f3ed-4f8a-bd95-cf026b89834d	resource_access.${client_id}.roles	claim.name
87be9ec0-f3ed-4f8a-bd95-cf026b89834d	String	jsonType.label
a618d5ed-7e33-41d3-b2e5-fe745c92459d	true	introspection.token.claim
a618d5ed-7e33-41d3-b2e5-fe745c92459d	true	multivalued
a618d5ed-7e33-41d3-b2e5-fe745c92459d	foo	user.attribute
a618d5ed-7e33-41d3-b2e5-fe745c92459d	true	access.token.claim
a618d5ed-7e33-41d3-b2e5-fe745c92459d	realm_access.roles	claim.name
a618d5ed-7e33-41d3-b2e5-fe745c92459d	String	jsonType.label
69a5dfc8-0f8a-4aa0-b7c6-73c1f790cf0d	true	introspection.token.claim
69a5dfc8-0f8a-4aa0-b7c6-73c1f790cf0d	true	access.token.claim
18a190b8-6388-406e-bd22-a20236ee1c08	true	introspection.token.claim
18a190b8-6388-406e-bd22-a20236ee1c08	true	multivalued
18a190b8-6388-406e-bd22-a20236ee1c08	foo	user.attribute
18a190b8-6388-406e-bd22-a20236ee1c08	true	id.token.claim
18a190b8-6388-406e-bd22-a20236ee1c08	true	access.token.claim
18a190b8-6388-406e-bd22-a20236ee1c08	groups	claim.name
18a190b8-6388-406e-bd22-a20236ee1c08	String	jsonType.label
1f190fcf-57fd-4dba-8049-7aa8dd43a52a	true	introspection.token.claim
1f190fcf-57fd-4dba-8049-7aa8dd43a52a	true	userinfo.token.claim
1f190fcf-57fd-4dba-8049-7aa8dd43a52a	username	user.attribute
1f190fcf-57fd-4dba-8049-7aa8dd43a52a	true	id.token.claim
1f190fcf-57fd-4dba-8049-7aa8dd43a52a	true	access.token.claim
1f190fcf-57fd-4dba-8049-7aa8dd43a52a	upn	claim.name
1f190fcf-57fd-4dba-8049-7aa8dd43a52a	String	jsonType.label
47faf84b-184c-40f0-bdbd-da14352589ec	true	introspection.token.claim
47faf84b-184c-40f0-bdbd-da14352589ec	true	id.token.claim
47faf84b-184c-40f0-bdbd-da14352589ec	true	access.token.claim
11d799a0-56c1-454b-8451-b7052932e198	true	introspection.token.claim
11d799a0-56c1-454b-8451-b7052932e198	true	access.token.claim
3e6d4d9b-eb0d-4c50-9fc0-700ffe944044	AUTH_TIME	user.session.note
3e6d4d9b-eb0d-4c50-9fc0-700ffe944044	true	introspection.token.claim
3e6d4d9b-eb0d-4c50-9fc0-700ffe944044	true	id.token.claim
3e6d4d9b-eb0d-4c50-9fc0-700ffe944044	true	access.token.claim
3e6d4d9b-eb0d-4c50-9fc0-700ffe944044	auth_time	claim.name
3e6d4d9b-eb0d-4c50-9fc0-700ffe944044	long	jsonType.label
3d947aa0-c00f-4e77-bd41-311968ca4dea	clientHost	user.session.note
3d947aa0-c00f-4e77-bd41-311968ca4dea	true	introspection.token.claim
3d947aa0-c00f-4e77-bd41-311968ca4dea	true	id.token.claim
3d947aa0-c00f-4e77-bd41-311968ca4dea	true	access.token.claim
3d947aa0-c00f-4e77-bd41-311968ca4dea	clientHost	claim.name
3d947aa0-c00f-4e77-bd41-311968ca4dea	String	jsonType.label
7314f796-8152-4194-b566-9ea48b84332b	client_id	user.session.note
7314f796-8152-4194-b566-9ea48b84332b	true	introspection.token.claim
7314f796-8152-4194-b566-9ea48b84332b	true	id.token.claim
7314f796-8152-4194-b566-9ea48b84332b	true	access.token.claim
7314f796-8152-4194-b566-9ea48b84332b	client_id	claim.name
7314f796-8152-4194-b566-9ea48b84332b	String	jsonType.label
a2ac6e6b-d806-48cd-bde6-c52fa567b72f	clientAddress	user.session.note
a2ac6e6b-d806-48cd-bde6-c52fa567b72f	true	introspection.token.claim
a2ac6e6b-d806-48cd-bde6-c52fa567b72f	true	id.token.claim
a2ac6e6b-d806-48cd-bde6-c52fa567b72f	true	access.token.claim
a2ac6e6b-d806-48cd-bde6-c52fa567b72f	clientAddress	claim.name
a2ac6e6b-d806-48cd-bde6-c52fa567b72f	String	jsonType.label
7f874995-f57c-42fd-a1b2-fadfe09239e7	true	introspection.token.claim
7f874995-f57c-42fd-a1b2-fadfe09239e7	true	multivalued
7f874995-f57c-42fd-a1b2-fadfe09239e7	true	id.token.claim
7f874995-f57c-42fd-a1b2-fadfe09239e7	true	access.token.claim
7f874995-f57c-42fd-a1b2-fadfe09239e7	organization	claim.name
7f874995-f57c-42fd-a1b2-fadfe09239e7	String	jsonType.label
f7ac5b9c-5dfd-4c92-b43d-e6d93615fa0a	true	introspection.token.claim
f7ac5b9c-5dfd-4c92-b43d-e6d93615fa0a	true	multivalued
f7ac5b9c-5dfd-4c92-b43d-e6d93615fa0a	true	userinfo.token.claim
f7ac5b9c-5dfd-4c92-b43d-e6d93615fa0a	true	id.token.claim
f7ac5b9c-5dfd-4c92-b43d-e6d93615fa0a	true	access.token.claim
f7ac5b9c-5dfd-4c92-b43d-e6d93615fa0a	organization	claim.name
f7ac5b9c-5dfd-4c92-b43d-e6d93615fa0a	String	jsonType.label
fe2c000d-31ce-4376-aea6-f623e185768f	false	single
fe2c000d-31ce-4376-aea6-f623e185768f	Basic	attribute.nameformat
fe2c000d-31ce-4376-aea6-f623e185768f	Role	attribute.name
c9c5128a-45b7-4154-9d6b-4ac92baa9789	true	access.token.claim
c9c5128a-45b7-4154-9d6b-4ac92baa9789	true	introspection.token.claim
174ea913-404e-4cd5-8aa2-e52de3e3f66c	foo	user.attribute
174ea913-404e-4cd5-8aa2-e52de3e3f66c	true	introspection.token.claim
174ea913-404e-4cd5-8aa2-e52de3e3f66c	true	access.token.claim
174ea913-404e-4cd5-8aa2-e52de3e3f66c	resource_access.${client_id}.roles	claim.name
174ea913-404e-4cd5-8aa2-e52de3e3f66c	String	jsonType.label
174ea913-404e-4cd5-8aa2-e52de3e3f66c	true	multivalued
640a3ec0-d2ab-447d-9e74-92648c6351ea	true	introspection.token.claim
640a3ec0-d2ab-447d-9e74-92648c6351ea	true	multivalued
640a3ec0-d2ab-447d-9e74-92648c6351ea	true	userinfo.token.claim
640a3ec0-d2ab-447d-9e74-92648c6351ea	foo	user.attribute
640a3ec0-d2ab-447d-9e74-92648c6351ea	true	id.token.claim
640a3ec0-d2ab-447d-9e74-92648c6351ea	true	access.token.claim
640a3ec0-d2ab-447d-9e74-92648c6351ea	realm_access.roles	claim.name
640a3ec0-d2ab-447d-9e74-92648c6351ea	String	jsonType.label
bbd7e124-5e2e-47c8-9713-3b810ad627f9	true	introspection.token.claim
bbd7e124-5e2e-47c8-9713-3b810ad627f9	true	access.token.claim
2cd8120e-4141-42d8-948f-fde701030d00	true	introspection.token.claim
2cd8120e-4141-42d8-948f-fde701030d00	true	userinfo.token.claim
2cd8120e-4141-42d8-948f-fde701030d00	username	user.attribute
2cd8120e-4141-42d8-948f-fde701030d00	true	id.token.claim
2cd8120e-4141-42d8-948f-fde701030d00	true	access.token.claim
2cd8120e-4141-42d8-948f-fde701030d00	upn	claim.name
2cd8120e-4141-42d8-948f-fde701030d00	String	jsonType.label
50496409-83c7-43cf-8055-44530f93c54e	true	introspection.token.claim
50496409-83c7-43cf-8055-44530f93c54e	true	multivalued
50496409-83c7-43cf-8055-44530f93c54e	true	userinfo.token.claim
50496409-83c7-43cf-8055-44530f93c54e	foo	user.attribute
50496409-83c7-43cf-8055-44530f93c54e	true	id.token.claim
50496409-83c7-43cf-8055-44530f93c54e	true	access.token.claim
50496409-83c7-43cf-8055-44530f93c54e	groups	claim.name
50496409-83c7-43cf-8055-44530f93c54e	String	jsonType.label
45056b20-b279-4c53-8843-52c068ada784	true	introspection.token.claim
45056b20-b279-4c53-8843-52c068ada784	true	access.token.claim
5ffaf19f-fc3b-472d-ba4f-b70578b86f93	AUTH_TIME	user.session.note
5ffaf19f-fc3b-472d-ba4f-b70578b86f93	true	introspection.token.claim
5ffaf19f-fc3b-472d-ba4f-b70578b86f93	true	userinfo.token.claim
5ffaf19f-fc3b-472d-ba4f-b70578b86f93	true	id.token.claim
5ffaf19f-fc3b-472d-ba4f-b70578b86f93	true	access.token.claim
5ffaf19f-fc3b-472d-ba4f-b70578b86f93	auth_time	claim.name
5ffaf19f-fc3b-472d-ba4f-b70578b86f93	long	jsonType.label
0d3926a8-e081-4f08-ba70-ac3f3b4f5d1f	true	introspection.token.claim
0d3926a8-e081-4f08-ba70-ac3f3b4f5d1f	true	userinfo.token.claim
0d3926a8-e081-4f08-ba70-ac3f3b4f5d1f	nickname	user.attribute
0d3926a8-e081-4f08-ba70-ac3f3b4f5d1f	true	id.token.claim
0d3926a8-e081-4f08-ba70-ac3f3b4f5d1f	true	access.token.claim
0d3926a8-e081-4f08-ba70-ac3f3b4f5d1f	nickname	claim.name
0d3926a8-e081-4f08-ba70-ac3f3b4f5d1f	String	jsonType.label
221c166c-b7f6-4674-a0f9-fe5fa9e1c552	true	introspection.token.claim
221c166c-b7f6-4674-a0f9-fe5fa9e1c552	true	userinfo.token.claim
221c166c-b7f6-4674-a0f9-fe5fa9e1c552	username	user.attribute
221c166c-b7f6-4674-a0f9-fe5fa9e1c552	true	id.token.claim
221c166c-b7f6-4674-a0f9-fe5fa9e1c552	true	access.token.claim
221c166c-b7f6-4674-a0f9-fe5fa9e1c552	preferred_username	claim.name
221c166c-b7f6-4674-a0f9-fe5fa9e1c552	String	jsonType.label
292b26b9-3570-44c2-90ab-789370a6bfde	true	id.token.claim
292b26b9-3570-44c2-90ab-789370a6bfde	true	introspection.token.claim
292b26b9-3570-44c2-90ab-789370a6bfde	true	access.token.claim
292b26b9-3570-44c2-90ab-789370a6bfde	true	userinfo.token.claim
34ae1958-66ca-4e5b-b704-a2685839834c	true	introspection.token.claim
34ae1958-66ca-4e5b-b704-a2685839834c	true	userinfo.token.claim
34ae1958-66ca-4e5b-b704-a2685839834c	gender	user.attribute
34ae1958-66ca-4e5b-b704-a2685839834c	true	id.token.claim
34ae1958-66ca-4e5b-b704-a2685839834c	true	access.token.claim
34ae1958-66ca-4e5b-b704-a2685839834c	gender	claim.name
34ae1958-66ca-4e5b-b704-a2685839834c	String	jsonType.label
5b4e2c0a-b29d-4a20-85bd-f05ac705ee32	true	introspection.token.claim
5b4e2c0a-b29d-4a20-85bd-f05ac705ee32	true	userinfo.token.claim
5b4e2c0a-b29d-4a20-85bd-f05ac705ee32	zoneinfo	user.attribute
5b4e2c0a-b29d-4a20-85bd-f05ac705ee32	true	id.token.claim
5b4e2c0a-b29d-4a20-85bd-f05ac705ee32	true	access.token.claim
5b4e2c0a-b29d-4a20-85bd-f05ac705ee32	zoneinfo	claim.name
5b4e2c0a-b29d-4a20-85bd-f05ac705ee32	String	jsonType.label
6dffadc9-89a7-4f79-8e1a-f75fdf7294a9	true	introspection.token.claim
6dffadc9-89a7-4f79-8e1a-f75fdf7294a9	true	userinfo.token.claim
6dffadc9-89a7-4f79-8e1a-f75fdf7294a9	picture	user.attribute
6dffadc9-89a7-4f79-8e1a-f75fdf7294a9	true	id.token.claim
6dffadc9-89a7-4f79-8e1a-f75fdf7294a9	true	access.token.claim
6dffadc9-89a7-4f79-8e1a-f75fdf7294a9	picture	claim.name
6dffadc9-89a7-4f79-8e1a-f75fdf7294a9	String	jsonType.label
6e8b96ac-e04f-41d1-a341-bf093d5aeb7b	true	introspection.token.claim
6e8b96ac-e04f-41d1-a341-bf093d5aeb7b	true	userinfo.token.claim
6e8b96ac-e04f-41d1-a341-bf093d5aeb7b	locale	user.attribute
6e8b96ac-e04f-41d1-a341-bf093d5aeb7b	true	id.token.claim
6e8b96ac-e04f-41d1-a341-bf093d5aeb7b	true	access.token.claim
6e8b96ac-e04f-41d1-a341-bf093d5aeb7b	locale	claim.name
6e8b96ac-e04f-41d1-a341-bf093d5aeb7b	String	jsonType.label
74135e06-87e9-45d2-b38f-99ca91554155	true	introspection.token.claim
74135e06-87e9-45d2-b38f-99ca91554155	true	userinfo.token.claim
74135e06-87e9-45d2-b38f-99ca91554155	website	user.attribute
74135e06-87e9-45d2-b38f-99ca91554155	true	id.token.claim
74135e06-87e9-45d2-b38f-99ca91554155	true	access.token.claim
74135e06-87e9-45d2-b38f-99ca91554155	website	claim.name
74135e06-87e9-45d2-b38f-99ca91554155	String	jsonType.label
782dea23-dd14-4d84-8cc2-877ff02179d9	true	introspection.token.claim
782dea23-dd14-4d84-8cc2-877ff02179d9	true	userinfo.token.claim
782dea23-dd14-4d84-8cc2-877ff02179d9	firstName	user.attribute
782dea23-dd14-4d84-8cc2-877ff02179d9	true	id.token.claim
782dea23-dd14-4d84-8cc2-877ff02179d9	true	access.token.claim
782dea23-dd14-4d84-8cc2-877ff02179d9	given_name	claim.name
782dea23-dd14-4d84-8cc2-877ff02179d9	String	jsonType.label
c75a2060-d8c9-483c-83a1-316e36b968eb	true	introspection.token.claim
c75a2060-d8c9-483c-83a1-316e36b968eb	true	userinfo.token.claim
c75a2060-d8c9-483c-83a1-316e36b968eb	lastName	user.attribute
c75a2060-d8c9-483c-83a1-316e36b968eb	true	id.token.claim
c75a2060-d8c9-483c-83a1-316e36b968eb	true	access.token.claim
c75a2060-d8c9-483c-83a1-316e36b968eb	family_name	claim.name
c75a2060-d8c9-483c-83a1-316e36b968eb	String	jsonType.label
c796224b-675e-4f85-92e0-911e2dd09338	true	introspection.token.claim
c796224b-675e-4f85-92e0-911e2dd09338	true	userinfo.token.claim
c796224b-675e-4f85-92e0-911e2dd09338	profile	user.attribute
c796224b-675e-4f85-92e0-911e2dd09338	true	id.token.claim
c796224b-675e-4f85-92e0-911e2dd09338	true	access.token.claim
c796224b-675e-4f85-92e0-911e2dd09338	profile	claim.name
c796224b-675e-4f85-92e0-911e2dd09338	String	jsonType.label
cca39f77-72ea-4890-afb3-10f52018227e	true	introspection.token.claim
cca39f77-72ea-4890-afb3-10f52018227e	true	userinfo.token.claim
cca39f77-72ea-4890-afb3-10f52018227e	updatedAt	user.attribute
cca39f77-72ea-4890-afb3-10f52018227e	true	id.token.claim
cca39f77-72ea-4890-afb3-10f52018227e	true	access.token.claim
cca39f77-72ea-4890-afb3-10f52018227e	updated_at	claim.name
cca39f77-72ea-4890-afb3-10f52018227e	long	jsonType.label
ce4a8627-24e7-4831-afa4-cdb1ad897637	true	introspection.token.claim
ce4a8627-24e7-4831-afa4-cdb1ad897637	true	userinfo.token.claim
ce4a8627-24e7-4831-afa4-cdb1ad897637	middleName	user.attribute
ce4a8627-24e7-4831-afa4-cdb1ad897637	true	id.token.claim
ce4a8627-24e7-4831-afa4-cdb1ad897637	true	access.token.claim
ce4a8627-24e7-4831-afa4-cdb1ad897637	middle_name	claim.name
ce4a8627-24e7-4831-afa4-cdb1ad897637	String	jsonType.label
e578983d-3343-4e07-b8be-58f52398777b	true	introspection.token.claim
e578983d-3343-4e07-b8be-58f52398777b	true	userinfo.token.claim
e578983d-3343-4e07-b8be-58f52398777b	birthdate	user.attribute
e578983d-3343-4e07-b8be-58f52398777b	true	id.token.claim
e578983d-3343-4e07-b8be-58f52398777b	true	access.token.claim
e578983d-3343-4e07-b8be-58f52398777b	birthdate	claim.name
e578983d-3343-4e07-b8be-58f52398777b	String	jsonType.label
a2d788f5-2b79-4268-a239-2708756f0675	true	introspection.token.claim
a2d788f5-2b79-4268-a239-2708756f0675	true	userinfo.token.claim
a2d788f5-2b79-4268-a239-2708756f0675	phoneNumber	user.attribute
a2d788f5-2b79-4268-a239-2708756f0675	true	id.token.claim
a2d788f5-2b79-4268-a239-2708756f0675	true	access.token.claim
a2d788f5-2b79-4268-a239-2708756f0675	phone_number	claim.name
a2d788f5-2b79-4268-a239-2708756f0675	String	jsonType.label
c7528bc7-aeb8-4c4a-b38f-42b5b58adbc8	true	introspection.token.claim
c7528bc7-aeb8-4c4a-b38f-42b5b58adbc8	true	userinfo.token.claim
c7528bc7-aeb8-4c4a-b38f-42b5b58adbc8	phoneNumberVerified	user.attribute
c7528bc7-aeb8-4c4a-b38f-42b5b58adbc8	true	id.token.claim
c7528bc7-aeb8-4c4a-b38f-42b5b58adbc8	true	access.token.claim
c7528bc7-aeb8-4c4a-b38f-42b5b58adbc8	phone_number_verified	claim.name
c7528bc7-aeb8-4c4a-b38f-42b5b58adbc8	boolean	jsonType.label
3588a16b-0d7c-4790-9c81-306b71a10d07	true	id.token.claim
3588a16b-0d7c-4790-9c81-306b71a10d07	true	access.token.claim
3588a16b-0d7c-4790-9c81-306b71a10d07	true	introspection.token.claim
3588a16b-0d7c-4790-9c81-306b71a10d07	true	userinfo.token.claim
2138f335-c272-4415-8bec-584d84cabdbb	client_id	user.session.note
2138f335-c272-4415-8bec-584d84cabdbb	true	introspection.token.claim
2138f335-c272-4415-8bec-584d84cabdbb	true	userinfo.token.claim
2138f335-c272-4415-8bec-584d84cabdbb	true	id.token.claim
2138f335-c272-4415-8bec-584d84cabdbb	true	access.token.claim
2138f335-c272-4415-8bec-584d84cabdbb	client_id	claim.name
2138f335-c272-4415-8bec-584d84cabdbb	String	jsonType.label
549f29c0-adc2-4695-ae1a-70ae30479837	clientAddress	user.session.note
549f29c0-adc2-4695-ae1a-70ae30479837	true	id.token.claim
549f29c0-adc2-4695-ae1a-70ae30479837	true	introspection.token.claim
549f29c0-adc2-4695-ae1a-70ae30479837	true	access.token.claim
549f29c0-adc2-4695-ae1a-70ae30479837	clientAddress	claim.name
549f29c0-adc2-4695-ae1a-70ae30479837	String	jsonType.label
59176ff1-9076-488a-a063-bf78600fa37f	clientHost	user.session.note
59176ff1-9076-488a-a063-bf78600fa37f	true	id.token.claim
59176ff1-9076-488a-a063-bf78600fa37f	true	introspection.token.claim
59176ff1-9076-488a-a063-bf78600fa37f	true	access.token.claim
59176ff1-9076-488a-a063-bf78600fa37f	clientHost	claim.name
59176ff1-9076-488a-a063-bf78600fa37f	String	jsonType.label
59176ff1-9076-488a-a063-bf78600fa37f	true	userinfo.token.claim
549f29c0-adc2-4695-ae1a-70ae30479837	true	userinfo.token.claim
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	formatted	user.attribute.formatted
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	country	user.attribute.country
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	true	introspection.token.claim
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	postal_code	user.attribute.postal_code
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	true	userinfo.token.claim
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	street	user.attribute.street
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	true	id.token.claim
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	region	user.attribute.region
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	true	access.token.claim
4fa4f2fc-1170-4ee0-81d7-b009832fffb1	locality	user.attribute.locality
a9cc5c7a-c2e8-44bd-b117-a521328ec607	true	introspection.token.claim
a9cc5c7a-c2e8-44bd-b117-a521328ec607	true	userinfo.token.claim
a9cc5c7a-c2e8-44bd-b117-a521328ec607	emailVerified	user.attribute
a9cc5c7a-c2e8-44bd-b117-a521328ec607	true	id.token.claim
a9cc5c7a-c2e8-44bd-b117-a521328ec607	true	access.token.claim
a9cc5c7a-c2e8-44bd-b117-a521328ec607	email_verified	claim.name
a9cc5c7a-c2e8-44bd-b117-a521328ec607	boolean	jsonType.label
dba5e1e9-96ff-468b-9c27-70665d8acd93	true	introspection.token.claim
dba5e1e9-96ff-468b-9c27-70665d8acd93	true	userinfo.token.claim
dba5e1e9-96ff-468b-9c27-70665d8acd93	email	user.attribute
dba5e1e9-96ff-468b-9c27-70665d8acd93	true	id.token.claim
dba5e1e9-96ff-468b-9c27-70665d8acd93	true	access.token.claim
dba5e1e9-96ff-468b-9c27-70665d8acd93	email	claim.name
dba5e1e9-96ff-468b-9c27-70665d8acd93	String	jsonType.label
73167c87-cee2-46e2-a5ca-57e85f395650	true	introspection.token.claim
73167c87-cee2-46e2-a5ca-57e85f395650	true	userinfo.token.claim
73167c87-cee2-46e2-a5ca-57e85f395650	locale	user.attribute
73167c87-cee2-46e2-a5ca-57e85f395650	true	id.token.claim
73167c87-cee2-46e2-a5ca-57e85f395650	true	access.token.claim
73167c87-cee2-46e2-a5ca-57e85f395650	locale	claim.name
73167c87-cee2-46e2-a5ca-57e85f395650	String	jsonType.label
\.


--
-- Data for Name: realm; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm (id, access_code_lifespan, user_action_lifespan, access_token_lifespan, account_theme, admin_theme, email_theme, enabled, events_enabled, events_expiration, login_theme, name, not_before, password_policy, registration_allowed, remember_me, reset_password_allowed, social, ssl_required, sso_idle_timeout, sso_max_lifespan, update_profile_on_soc_login, verify_email, master_admin_client, login_lifespan, internationalization_enabled, default_locale, reg_email_as_username, admin_events_enabled, admin_events_details_enabled, edit_username_allowed, otp_policy_counter, otp_policy_window, otp_policy_period, otp_policy_digits, otp_policy_alg, otp_policy_type, browser_flow, registration_flow, direct_grant_flow, reset_credentials_flow, client_auth_flow, offline_session_idle_timeout, revoke_refresh_token, access_token_life_implicit, login_with_email_allowed, duplicate_emails_allowed, docker_auth_flow, refresh_token_max_reuse, allow_user_managed_access, sso_max_lifespan_remember_me, sso_idle_timeout_remember_me, default_role) FROM stdin;
950f7f4b-1af6-4a64-bb5e-2561faa87127	60	300	60	\N	\N	\N	t	f	0	\N	master	0	\N	f	f	f	f	EXTERNAL	1800	36000	f	f	a8ce899c-8a3d-4391-98dc-72610c85b515	1800	f	\N	f	f	f	f	0	1	30	6	HmacSHA1	totp	61626dbf-8b26-4c8b-b9db-e12daabdeb09	fbe0f1b4-4288-48a7-8d9e-4b83a347b8f0	522bdc6c-fb12-4b94-8d75-666ad8a60185	275b1fe4-338d-4c87-9707-5c6008b60fcc	6c6e1bff-c862-4bde-b219-7877e79fdbb2	2592000	f	900	t	f	fdeb50ca-1ec0-4808-96c8-6587bdfdb939	0	f	0	0	33aa8679-f89d-47ee-8e63-d57d79270440
c55a12d3-a06b-43f4-b990-28390a55a7af	60	300	300	\N	\N	\N	t	t	7200	\N	csfeer	0	\N	f	f	f	f	EXTERNAL	1800	36000	f	f	ce82e997-d439-4acf-8d80-8c0ed9b401b4	1800	f	\N	f	f	f	f	0	1	30	6	HmacSHA1	totp	f9d5cc86-3825-47cf-ae7f-c07abe687f11	90668b03-0d53-453d-98c7-312f13d16cf5	2f47735e-097d-420e-8486-33b13e85bddb	dfcd5483-03a4-4ca1-97ed-275d9e35434c	5ceaf82b-70da-4968-b87b-129337abe077	2592000	f	900	t	f	2c5bf88c-6a6b-449b-9f84-b62d149a9291	0	f	0	0	e4a418ce-31f7-4051-a751-eccb5a7e7f8a
\.


--
-- Data for Name: realm_attribute; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm_attribute (name, realm_id, value) FROM stdin;
_browser_header.contentSecurityPolicyReportOnly	950f7f4b-1af6-4a64-bb5e-2561faa87127	
_browser_header.xContentTypeOptions	950f7f4b-1af6-4a64-bb5e-2561faa87127	nosniff
_browser_header.referrerPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	no-referrer
_browser_header.xRobotsTag	950f7f4b-1af6-4a64-bb5e-2561faa87127	none
_browser_header.xFrameOptions	950f7f4b-1af6-4a64-bb5e-2561faa87127	SAMEORIGIN
_browser_header.contentSecurityPolicy	950f7f4b-1af6-4a64-bb5e-2561faa87127	frame-src 'self'; frame-ancestors 'self'; object-src 'none';
_browser_header.strictTransportSecurity	950f7f4b-1af6-4a64-bb5e-2561faa87127	max-age=31536000; includeSubDomains
bruteForceProtected	950f7f4b-1af6-4a64-bb5e-2561faa87127	false
permanentLockout	950f7f4b-1af6-4a64-bb5e-2561faa87127	false
maxTemporaryLockouts	950f7f4b-1af6-4a64-bb5e-2561faa87127	0
bruteForceStrategy	950f7f4b-1af6-4a64-bb5e-2561faa87127	MULTIPLE
maxFailureWaitSeconds	950f7f4b-1af6-4a64-bb5e-2561faa87127	900
minimumQuickLoginWaitSeconds	950f7f4b-1af6-4a64-bb5e-2561faa87127	60
waitIncrementSeconds	950f7f4b-1af6-4a64-bb5e-2561faa87127	60
quickLoginCheckMilliSeconds	950f7f4b-1af6-4a64-bb5e-2561faa87127	1000
maxDeltaTimeSeconds	950f7f4b-1af6-4a64-bb5e-2561faa87127	43200
failureFactor	950f7f4b-1af6-4a64-bb5e-2561faa87127	30
realmReusableOtpCode	950f7f4b-1af6-4a64-bb5e-2561faa87127	false
firstBrokerLoginFlowId	950f7f4b-1af6-4a64-bb5e-2561faa87127	a0df8b1b-ad8f-4648-a70a-90679d1ada73
displayName	950f7f4b-1af6-4a64-bb5e-2561faa87127	Keycloak
displayNameHtml	950f7f4b-1af6-4a64-bb5e-2561faa87127	<div class="kc-logo-text"><span>Keycloak</span></div>
defaultSignatureAlgorithm	950f7f4b-1af6-4a64-bb5e-2561faa87127	RS256
offlineSessionMaxLifespanEnabled	950f7f4b-1af6-4a64-bb5e-2561faa87127	false
offlineSessionMaxLifespan	950f7f4b-1af6-4a64-bb5e-2561faa87127	5184000
_browser_header.contentSecurityPolicyReportOnly	c55a12d3-a06b-43f4-b990-28390a55a7af	
_browser_header.xContentTypeOptions	c55a12d3-a06b-43f4-b990-28390a55a7af	nosniff
_browser_header.referrerPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	no-referrer
_browser_header.xRobotsTag	c55a12d3-a06b-43f4-b990-28390a55a7af	none
_browser_header.xFrameOptions	c55a12d3-a06b-43f4-b990-28390a55a7af	SAMEORIGIN
_browser_header.contentSecurityPolicy	c55a12d3-a06b-43f4-b990-28390a55a7af	frame-src 'self'; frame-ancestors 'self'; object-src 'none';
_browser_header.strictTransportSecurity	c55a12d3-a06b-43f4-b990-28390a55a7af	max-age=31536000; includeSubDomains
bruteForceProtected	c55a12d3-a06b-43f4-b990-28390a55a7af	false
permanentLockout	c55a12d3-a06b-43f4-b990-28390a55a7af	false
maxTemporaryLockouts	c55a12d3-a06b-43f4-b990-28390a55a7af	0
bruteForceStrategy	c55a12d3-a06b-43f4-b990-28390a55a7af	MULTIPLE
maxFailureWaitSeconds	c55a12d3-a06b-43f4-b990-28390a55a7af	900
minimumQuickLoginWaitSeconds	c55a12d3-a06b-43f4-b990-28390a55a7af	60
waitIncrementSeconds	c55a12d3-a06b-43f4-b990-28390a55a7af	60
quickLoginCheckMilliSeconds	c55a12d3-a06b-43f4-b990-28390a55a7af	1000
maxDeltaTimeSeconds	c55a12d3-a06b-43f4-b990-28390a55a7af	43200
failureFactor	c55a12d3-a06b-43f4-b990-28390a55a7af	30
realmReusableOtpCode	c55a12d3-a06b-43f4-b990-28390a55a7af	false
defaultSignatureAlgorithm	c55a12d3-a06b-43f4-b990-28390a55a7af	RS256
offlineSessionMaxLifespanEnabled	c55a12d3-a06b-43f4-b990-28390a55a7af	false
offlineSessionMaxLifespan	c55a12d3-a06b-43f4-b990-28390a55a7af	5184000
clientSessionIdleTimeout	c55a12d3-a06b-43f4-b990-28390a55a7af	0
clientSessionMaxLifespan	c55a12d3-a06b-43f4-b990-28390a55a7af	0
clientOfflineSessionIdleTimeout	c55a12d3-a06b-43f4-b990-28390a55a7af	0
clientOfflineSessionMaxLifespan	c55a12d3-a06b-43f4-b990-28390a55a7af	0
actionTokenGeneratedByAdminLifespan	c55a12d3-a06b-43f4-b990-28390a55a7af	43200
actionTokenGeneratedByUserLifespan	c55a12d3-a06b-43f4-b990-28390a55a7af	300
oauth2DeviceCodeLifespan	c55a12d3-a06b-43f4-b990-28390a55a7af	600
oauth2DevicePollingInterval	c55a12d3-a06b-43f4-b990-28390a55a7af	5
organizationsEnabled	c55a12d3-a06b-43f4-b990-28390a55a7af	false
adminPermissionsEnabled	c55a12d3-a06b-43f4-b990-28390a55a7af	false
webAuthnPolicyRpEntityName	c55a12d3-a06b-43f4-b990-28390a55a7af	keycloak
webAuthnPolicySignatureAlgorithms	c55a12d3-a06b-43f4-b990-28390a55a7af	ES256,RS256
webAuthnPolicyRpId	c55a12d3-a06b-43f4-b990-28390a55a7af	
webAuthnPolicyAttestationConveyancePreference	c55a12d3-a06b-43f4-b990-28390a55a7af	not specified
webAuthnPolicyAuthenticatorAttachment	c55a12d3-a06b-43f4-b990-28390a55a7af	not specified
webAuthnPolicyRequireResidentKey	c55a12d3-a06b-43f4-b990-28390a55a7af	not specified
webAuthnPolicyUserVerificationRequirement	c55a12d3-a06b-43f4-b990-28390a55a7af	not specified
webAuthnPolicyCreateTimeout	c55a12d3-a06b-43f4-b990-28390a55a7af	0
webAuthnPolicyAvoidSameAuthenticatorRegister	c55a12d3-a06b-43f4-b990-28390a55a7af	false
webAuthnPolicyRpEntityNamePasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	keycloak
webAuthnPolicySignatureAlgorithmsPasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	ES256,RS256
webAuthnPolicyRpIdPasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	
webAuthnPolicyAttestationConveyancePreferencePasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	not specified
webAuthnPolicyAuthenticatorAttachmentPasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	not specified
webAuthnPolicyRequireResidentKeyPasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	not specified
webAuthnPolicyUserVerificationRequirementPasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	not specified
webAuthnPolicyCreateTimeoutPasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	0
webAuthnPolicyAvoidSameAuthenticatorRegisterPasswordless	c55a12d3-a06b-43f4-b990-28390a55a7af	false
cibaBackchannelTokenDeliveryMode	c55a12d3-a06b-43f4-b990-28390a55a7af	poll
cibaExpiresIn	c55a12d3-a06b-43f4-b990-28390a55a7af	120
cibaInterval	c55a12d3-a06b-43f4-b990-28390a55a7af	5
cibaAuthRequestedUserHint	c55a12d3-a06b-43f4-b990-28390a55a7af	login_hint
parRequestUriLifespan	c55a12d3-a06b-43f4-b990-28390a55a7af	60
firstBrokerLoginFlowId	c55a12d3-a06b-43f4-b990-28390a55a7af	385da139-ce9e-469b-81a9-37e9e765c315
verifiableCredentialsEnabled	c55a12d3-a06b-43f4-b990-28390a55a7af	false
client-policies.profiles	c55a12d3-a06b-43f4-b990-28390a55a7af	{"profiles":[]}
client-policies.policies	c55a12d3-a06b-43f4-b990-28390a55a7af	{"policies":[]}
\.


--
-- Data for Name: realm_default_groups; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm_default_groups (realm_id, group_id) FROM stdin;
\.


--
-- Data for Name: realm_enabled_event_types; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm_enabled_event_types (realm_id, value) FROM stdin;
c55a12d3-a06b-43f4-b990-28390a55a7af	SEND_RESET_PASSWORD
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_CONSENT_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	GRANT_CONSENT
c55a12d3-a06b-43f4-b990-28390a55a7af	VERIFY_PROFILE_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	REMOVE_TOTP
c55a12d3-a06b-43f4-b990-28390a55a7af	REVOKE_GRANT
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_TOTP
c55a12d3-a06b-43f4-b990-28390a55a7af	LOGIN_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_LOGIN
c55a12d3-a06b-43f4-b990-28390a55a7af	RESET_PASSWORD_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_CREDENTIAL
c55a12d3-a06b-43f4-b990-28390a55a7af	IMPERSONATE_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	CODE_TO_TOKEN_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	CUSTOM_REQUIRED_ACTION
c55a12d3-a06b-43f4-b990-28390a55a7af	OAUTH2_DEVICE_CODE_TO_TOKEN_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	RESTART_AUTHENTICATION
c55a12d3-a06b-43f4-b990-28390a55a7af	IMPERSONATE
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_PROFILE_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	LOGIN
c55a12d3-a06b-43f4-b990-28390a55a7af	OAUTH2_DEVICE_VERIFY_USER_CODE
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_PASSWORD_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_INITIATED_ACCOUNT_LINKING
c55a12d3-a06b-43f4-b990-28390a55a7af	IDENTITY_PROVIDER_LOGIN
c55a12d3-a06b-43f4-b990-28390a55a7af	OAUTH2_EXTENSION_GRANT
c55a12d3-a06b-43f4-b990-28390a55a7af	USER_DISABLED_BY_PERMANENT_LOCKOUT
c55a12d3-a06b-43f4-b990-28390a55a7af	REMOVE_CREDENTIAL_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	TOKEN_EXCHANGE
c55a12d3-a06b-43f4-b990-28390a55a7af	AUTHREQID_TO_TOKEN
c55a12d3-a06b-43f4-b990-28390a55a7af	LOGOUT
c55a12d3-a06b-43f4-b990-28390a55a7af	REGISTER
c55a12d3-a06b-43f4-b990-28390a55a7af	DELETE_ACCOUNT_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_REGISTER
c55a12d3-a06b-43f4-b990-28390a55a7af	IDENTITY_PROVIDER_LINK_ACCOUNT
c55a12d3-a06b-43f4-b990-28390a55a7af	USER_DISABLED_BY_TEMPORARY_LOCKOUT
c55a12d3-a06b-43f4-b990-28390a55a7af	DELETE_ACCOUNT
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_PASSWORD
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_DELETE
c55a12d3-a06b-43f4-b990-28390a55a7af	FEDERATED_IDENTITY_LINK_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	IDENTITY_PROVIDER_FIRST_LOGIN
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_DELETE_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	VERIFY_EMAIL
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_LOGIN_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	RESTART_AUTHENTICATION_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	EXECUTE_ACTIONS
c55a12d3-a06b-43f4-b990-28390a55a7af	REMOVE_FEDERATED_IDENTITY_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	TOKEN_EXCHANGE_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	PERMISSION_TOKEN
c55a12d3-a06b-43f4-b990-28390a55a7af	FEDERATED_IDENTITY_OVERRIDE_LINK
c55a12d3-a06b-43f4-b990-28390a55a7af	SEND_IDENTITY_PROVIDER_LINK_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_CREDENTIAL_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	EXECUTE_ACTION_TOKEN_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	OAUTH2_EXTENSION_GRANT_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	SEND_VERIFY_EMAIL
c55a12d3-a06b-43f4-b990-28390a55a7af	OAUTH2_DEVICE_AUTH
c55a12d3-a06b-43f4-b990-28390a55a7af	EXECUTE_ACTIONS_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	REMOVE_FEDERATED_IDENTITY
c55a12d3-a06b-43f4-b990-28390a55a7af	OAUTH2_DEVICE_CODE_TO_TOKEN
c55a12d3-a06b-43f4-b990-28390a55a7af	IDENTITY_PROVIDER_POST_LOGIN
c55a12d3-a06b-43f4-b990-28390a55a7af	IDENTITY_PROVIDER_LINK_ACCOUNT_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	FEDERATED_IDENTITY_OVERRIDE_LINK_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	OAUTH2_DEVICE_VERIFY_USER_CODE_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_EMAIL
c55a12d3-a06b-43f4-b990-28390a55a7af	REGISTER_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	REVOKE_GRANT_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	EXECUTE_ACTION_TOKEN
c55a12d3-a06b-43f4-b990-28390a55a7af	LOGOUT_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_EMAIL_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_UPDATE_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	AUTHREQID_TO_TOKEN_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	INVITE_ORG_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_PROFILE
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_REGISTER_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	FEDERATED_IDENTITY_LINK
c55a12d3-a06b-43f4-b990-28390a55a7af	INVITE_ORG
c55a12d3-a06b-43f4-b990-28390a55a7af	SEND_IDENTITY_PROVIDER_LINK
c55a12d3-a06b-43f4-b990-28390a55a7af	SEND_VERIFY_EMAIL_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	IDENTITY_PROVIDER_LOGIN_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	RESET_PASSWORD
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_INITIATED_ACCOUNT_LINKING_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	OAUTH2_DEVICE_AUTH_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	REMOVE_CREDENTIAL
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_CONSENT
c55a12d3-a06b-43f4-b990-28390a55a7af	REMOVE_TOTP_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	VERIFY_EMAIL_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	SEND_RESET_PASSWORD_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	CLIENT_UPDATE
c55a12d3-a06b-43f4-b990-28390a55a7af	CUSTOM_REQUIRED_ACTION_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	IDENTITY_PROVIDER_POST_LOGIN_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	UPDATE_TOTP_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	CODE_TO_TOKEN
c55a12d3-a06b-43f4-b990-28390a55a7af	VERIFY_PROFILE
c55a12d3-a06b-43f4-b990-28390a55a7af	GRANT_CONSENT_ERROR
c55a12d3-a06b-43f4-b990-28390a55a7af	IDENTITY_PROVIDER_FIRST_LOGIN_ERROR
\.


--
-- Data for Name: realm_events_listeners; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm_events_listeners (realm_id, value) FROM stdin;
950f7f4b-1af6-4a64-bb5e-2561faa87127	jboss-logging
c55a12d3-a06b-43f4-b990-28390a55a7af	jboss-logging
\.


--
-- Data for Name: realm_localizations; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm_localizations (realm_id, locale, texts) FROM stdin;
\.


--
-- Data for Name: realm_required_credential; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm_required_credential (type, form_label, input, secret, realm_id) FROM stdin;
password	password	t	t	950f7f4b-1af6-4a64-bb5e-2561faa87127
password	password	t	t	c55a12d3-a06b-43f4-b990-28390a55a7af
\.


--
-- Data for Name: realm_smtp_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm_smtp_config (realm_id, value, name) FROM stdin;
\.


--
-- Data for Name: realm_supported_locales; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.realm_supported_locales (realm_id, value) FROM stdin;
\.


--
-- Data for Name: redirect_uris; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.redirect_uris (client_id, value) FROM stdin;
70f8e924-f945-4a2a-b7f2-130505a5f8f7	/realms/master/account/*
640d1fae-9a47-46dc-81d3-8ed39870984a	/realms/master/account/*
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	/admin/master/console/*
3a97fb4a-6f6e-4174-bcf3-d80116bb5036	/realms/csfeer/account/*
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	/realms/csfeer/account/*
043917f3-a51e-4661-83c1-41b19f4ee3fe	/admin/csfeer/console/*
83ab17ea-566c-43b4-abc5-847346d7485a	http://ui.csfeer:8000/oidc/callback
83ab17ea-566c-43b4-abc5-847346d7485a	http://localhost:8000/oidc/callback
83ab17ea-566c-43b4-abc5-847346d7485a	http://127.0.0.1:8000/oidc/callback
\.


--
-- Data for Name: required_action_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.required_action_config (required_action_id, value, name) FROM stdin;
\.


--
-- Data for Name: required_action_provider; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.required_action_provider (id, alias, name, realm_id, enabled, default_action, provider_id, priority) FROM stdin;
bd2ddf02-65de-45cc-b715-e522c9760632	VERIFY_EMAIL	Verify Email	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	VERIFY_EMAIL	50
909ac9a6-3914-498a-9200-d165463a7db8	UPDATE_PROFILE	Update Profile	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	UPDATE_PROFILE	40
6c3f2c1f-f98c-484a-a4cf-1adf07082f16	CONFIGURE_TOTP	Configure OTP	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	CONFIGURE_TOTP	10
3e4bc62c-ab02-4a02-bcba-521e7396925e	UPDATE_PASSWORD	Update Password	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	UPDATE_PASSWORD	30
23196e65-e7d2-4cd0-b310-2973186473af	TERMS_AND_CONDITIONS	Terms and Conditions	950f7f4b-1af6-4a64-bb5e-2561faa87127	f	f	TERMS_AND_CONDITIONS	20
8465ff0a-f94c-4111-a0ec-37a2a92c05b9	delete_account	Delete Account	950f7f4b-1af6-4a64-bb5e-2561faa87127	f	f	delete_account	60
6626a1f6-8128-41ee-91bd-b74c85ee4cc6	delete_credential	Delete Credential	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	delete_credential	110
c0ffe254-ea56-412e-82f3-6cb196591690	update_user_locale	Update User Locale	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	update_user_locale	1000
700ff758-9c10-42f0-baac-2600dac97dad	UPDATE_EMAIL	Update Email	950f7f4b-1af6-4a64-bb5e-2561faa87127	f	f	UPDATE_EMAIL	70
77981725-f22c-4508-a7b7-0bea12bbc248	CONFIGURE_RECOVERY_AUTHN_CODES	Recovery Authentication Codes	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	CONFIGURE_RECOVERY_AUTHN_CODES	130
3eda0e92-ed54-470e-9371-246eb29ebdd8	webauthn-register	Webauthn Register	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	webauthn-register	80
72d40d09-c59f-467a-ba72-de6d1c1e9a19	webauthn-register-passwordless	Webauthn Register Passwordless	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	webauthn-register-passwordless	90
ab7124b4-b6c3-46a2-94d2-ce8eb29e0388	VERIFY_PROFILE	Verify Profile	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	VERIFY_PROFILE	100
b7cd49d3-0a46-413d-9dbe-30bb40ce3770	idp_link	Linking Identity Provider	950f7f4b-1af6-4a64-bb5e-2561faa87127	t	f	idp_link	120
4c09357b-b46b-40d4-bb0d-70b69139a2bb	CONFIGURE_TOTP	Configure OTP	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	CONFIGURE_TOTP	10
bc51231f-3442-41e3-9a35-e30fd65c628b	TERMS_AND_CONDITIONS	Terms and Conditions	c55a12d3-a06b-43f4-b990-28390a55a7af	f	f	TERMS_AND_CONDITIONS	20
43a3390c-15dc-484c-8cb8-62f8a9cc8449	UPDATE_PASSWORD	Update Password	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	UPDATE_PASSWORD	30
2da3121c-dda0-4228-baf7-bfa28121ef88	UPDATE_PROFILE	Update Profile	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	UPDATE_PROFILE	40
d2d9df07-2364-478e-a0df-930aead27881	VERIFY_EMAIL	Verify Email	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	VERIFY_EMAIL	50
4cd76a3b-d30c-42a7-ba64-33f7e3dc8444	delete_account	Delete Account	c55a12d3-a06b-43f4-b990-28390a55a7af	f	f	delete_account	60
5e6faf3e-ba2c-42eb-b584-1c0ec0b1ea83	webauthn-register	Webauthn Register	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	webauthn-register	70
278f9a64-65f8-44ef-bb12-3e8fb269073b	webauthn-register-passwordless	Webauthn Register Passwordless	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	webauthn-register-passwordless	80
089fd702-09ee-4265-928e-dfca08cb6fba	VERIFY_PROFILE	Verify Profile	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	VERIFY_PROFILE	90
27f963b0-c643-4410-bdca-ac81000102c2	delete_credential	Delete Credential	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	delete_credential	100
1c0ab926-8442-4b8b-9a9b-b2bc8e969046	idp_link	Linking Identity Provider	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	idp_link	110
05ecc31a-4012-44fe-9b87-d61631c14647	CONFIGURE_RECOVERY_AUTHN_CODES	Recovery Authentication Codes	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	CONFIGURE_RECOVERY_AUTHN_CODES	120
a6d86c94-f99c-463b-bbf6-65cfdff37863	update_user_locale	Update User Locale	c55a12d3-a06b-43f4-b990-28390a55a7af	t	f	update_user_locale	1000
\.


--
-- Data for Name: resource_attribute; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_attribute (id, name, value, resource_id) FROM stdin;
\.


--
-- Data for Name: resource_policy; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_policy (resource_id, policy_id) FROM stdin;
\.


--
-- Data for Name: resource_scope; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_scope (resource_id, scope_id) FROM stdin;
\.


--
-- Data for Name: resource_server; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_server (id, allow_rs_remote_mgmt, policy_enforce_mode, decision_strategy) FROM stdin;
\.


--
-- Data for Name: resource_server_perm_ticket; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_server_perm_ticket (id, owner, requester, created_timestamp, granted_timestamp, resource_id, scope_id, resource_server_id, policy_id) FROM stdin;
\.


--
-- Data for Name: resource_server_policy; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_server_policy (id, name, description, type, decision_strategy, logic, resource_server_id, owner) FROM stdin;
\.


--
-- Data for Name: resource_server_resource; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_server_resource (id, name, type, icon_uri, owner, resource_server_id, owner_managed_access, display_name) FROM stdin;
\.


--
-- Data for Name: resource_server_scope; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_server_scope (id, name, icon_uri, resource_server_id, display_name) FROM stdin;
\.


--
-- Data for Name: resource_uris; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.resource_uris (resource_id, value) FROM stdin;
\.


--
-- Data for Name: revoked_token; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.revoked_token (id, expire) FROM stdin;
\.


--
-- Data for Name: role_attribute; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.role_attribute (id, role_id, name, value) FROM stdin;
\.


--
-- Data for Name: scope_mapping; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.scope_mapping (client_id, role_id) FROM stdin;
640d1fae-9a47-46dc-81d3-8ed39870984a	27737e8a-5ec2-4c3f-b929-725240133d56
640d1fae-9a47-46dc-81d3-8ed39870984a	b7b08417-b998-4183-8c77-7122fbc93c8a
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	1dec6fcb-0eec-473f-8a1c-e3c12ebcd73e
c003a982-e593-4ee1-9a4c-02fd6c6b29fa	3d831730-fb07-4e8e-8afb-1f6060f7beae
\.


--
-- Data for Name: scope_policy; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.scope_policy (scope_id, policy_id) FROM stdin;
\.


--
-- Data for Name: server_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.server_config (server_config_key, value, version) FROM stdin;
\.


--
-- Data for Name: user_attribute; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_attribute (name, value, user_id, id, long_value_hash, long_value_hash_lower_case, long_value) FROM stdin;
is_temporary_admin	true	dad2c622-f878-4d62-8ae2-39bfe52003ae	15b7da3b-8a75-4ffc-b9f5-99622ed3efe9	\N	\N	\N
\.


--
-- Data for Name: user_consent; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_consent (id, client_id, user_id, created_date, last_updated_date, client_storage_provider, external_client_id) FROM stdin;
\.


--
-- Data for Name: user_consent_client_scope; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_consent_client_scope (user_consent_id, scope_id) FROM stdin;
\.


--
-- Data for Name: user_entity; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_entity (id, email, email_constraint, email_verified, enabled, federation_link, first_name, last_name, realm_id, username, created_timestamp, service_account_client_link, not_before) FROM stdin;
dad2c622-f878-4d62-8ae2-39bfe52003ae	\N	7d3247f7-466f-4143-835c-a4dfb56ba880	f	t	\N	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	admin	1777560081331	\N	0
185ee280-bc1b-4955-b5f7-be987b95842e	\N	471e1775-5e0a-474d-a030-ea6c6e766217	f	t	\N	\N	\N	950f7f4b-1af6-4a64-bb5e-2561faa87127	service-account-csfeer-auth	1777560081426	b10fcaff-5d8e-435c-b79f-04c0d2ae6da6	0
392ff97d-168a-4526-af46-bc10528b7962	admin@example.com	admin@example.com	t	t	\N	admin	admin	c55a12d3-a06b-43f4-b990-28390a55a7af	admin	1777560083731	\N	0
8a4d8b38-9999-49c9-bcbe-c30bb730b53c	demo@example.com	demo@example.com	t	t	\N	demo	demo	c55a12d3-a06b-43f4-b990-28390a55a7af	demo	1777560085352	\N	0
602688a7-1050-4a44-8633-cb58f2b0625a	demo-1@example.com	demo-1@example.com	t	t	\N	demo-1	demo-1	c55a12d3-a06b-43f4-b990-28390a55a7af	demo-1	1777560087055	\N	0
d2f94b3d-be17-4a59-aa5a-8373bc7aea4c	demo-2@example.com	demo-2@example.com	t	t	\N	demo-2	demo-2	c55a12d3-a06b-43f4-b990-28390a55a7af	demo-2	1777560088846	\N	0
3ef46cae-90b7-4930-a8fb-43e6e19c0aa7	recipient-viewer@example.com	recipient-viewer@example.com	t	t	\N	recipient-viewer	recipient-viewer	c55a12d3-a06b-43f4-b990-28390a55a7af	recipient-viewer	1777560090528	\N	0
1f2bad2b-bc71-4e74-abbd-31702831125e	recipient-editor@example.com	recipient-editor@example.com	t	t	\N	recipient-editor	recipient-editor	c55a12d3-a06b-43f4-b990-28390a55a7af	recipient-editor	1777560092150	\N	0
18e39e37-b032-4221-b99a-852900598c3d	recipient-approver@example.com	recipient-approver@example.com	t	t	\N	recipient-approver	recipient-approver	c55a12d3-a06b-43f4-b990-28390a55a7af	recipient-approver	1777560093870	\N	0
9dd77269-24e5-4698-b16e-3a8b4ad7500a	recipient-ao@example.com	recipient-ao@example.com	t	t	\N	recipient-ao	recipient-ao	c55a12d3-a06b-43f4-b990-28390a55a7af	recipient-ao	1777560095517	\N	0
\.


--
-- Data for Name: user_federation_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_federation_config (user_federation_provider_id, value, name) FROM stdin;
\.


--
-- Data for Name: user_federation_mapper; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_federation_mapper (id, name, federation_provider_id, federation_mapper_type, realm_id) FROM stdin;
\.


--
-- Data for Name: user_federation_mapper_config; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_federation_mapper_config (user_federation_mapper_id, value, name) FROM stdin;
\.


--
-- Data for Name: user_federation_provider; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_federation_provider (id, changed_sync_period, display_name, full_sync_period, last_sync, priority, provider_name, realm_id) FROM stdin;
\.


--
-- Data for Name: user_group_membership; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_group_membership (group_id, user_id, membership_type) FROM stdin;
\.


--
-- Data for Name: user_required_action; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_required_action (user_id, required_action) FROM stdin;
\.


--
-- Data for Name: user_role_mapping; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.user_role_mapping (role_id, user_id) FROM stdin;
33aa8679-f89d-47ee-8e63-d57d79270440	dad2c622-f878-4d62-8ae2-39bfe52003ae
36c982d0-3c1d-4472-95f5-63f2f2554ee6	dad2c622-f878-4d62-8ae2-39bfe52003ae
33aa8679-f89d-47ee-8e63-d57d79270440	185ee280-bc1b-4955-b5f7-be987b95842e
36c982d0-3c1d-4472-95f5-63f2f2554ee6	185ee280-bc1b-4955-b5f7-be987b95842e
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	392ff97d-168a-4526-af46-bc10528b7962
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	8a4d8b38-9999-49c9-bcbe-c30bb730b53c
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	602688a7-1050-4a44-8633-cb58f2b0625a
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	d2f94b3d-be17-4a59-aa5a-8373bc7aea4c
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	3ef46cae-90b7-4930-a8fb-43e6e19c0aa7
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	1f2bad2b-bc71-4e74-abbd-31702831125e
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	18e39e37-b032-4221-b99a-852900598c3d
e4a418ce-31f7-4051-a751-eccb5a7e7f8a	9dd77269-24e5-4698-b16e-3a8b4ad7500a
\.


--
-- Data for Name: web_origins; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.web_origins (client_id, value) FROM stdin;
1019acd8-53d9-4ee6-959a-9a5b4660bdc1	+
043917f3-a51e-4661-83c1-41b19f4ee3fe	+
83ab17ea-566c-43b4-abc5-847346d7485a	http://ui.csfeer:8000
83ab17ea-566c-43b4-abc5-847346d7485a	http://127.0.0.1:8000
83ab17ea-566c-43b4-abc5-847346d7485a	http://localhost:8000
\.


--
-- Data for Name: workflow_state; Type: TABLE DATA; Schema: public; Owner: csfeer
--

COPY public.workflow_state (execution_id, resource_id, workflow_id, resource_type, scheduled_step_id, scheduled_step_timestamp) FROM stdin;
\.


--
-- Name: org_domain ORG_DOMAIN_pkey; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.org_domain
    ADD CONSTRAINT "ORG_DOMAIN_pkey" PRIMARY KEY (id, name);


--
-- Name: org ORG_pkey; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.org
    ADD CONSTRAINT "ORG_pkey" PRIMARY KEY (id);


--
-- Name: server_config SERVER_CONFIG_pkey; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.server_config
    ADD CONSTRAINT "SERVER_CONFIG_pkey" PRIMARY KEY (server_config_key);


--
-- Name: keycloak_role UK_J3RWUVD56ONTGSUHOGM184WW2-2; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.keycloak_role
    ADD CONSTRAINT "UK_J3RWUVD56ONTGSUHOGM184WW2-2" UNIQUE (name, client_realm_constraint);


--
-- Name: client_auth_flow_bindings c_cli_flow_bind; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_auth_flow_bindings
    ADD CONSTRAINT c_cli_flow_bind PRIMARY KEY (client_id, binding_name);


--
-- Name: client_scope_client c_cli_scope_bind; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_scope_client
    ADD CONSTRAINT c_cli_scope_bind PRIMARY KEY (client_id, scope_id);


--
-- Name: client_initial_access cnstr_client_init_acc_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_initial_access
    ADD CONSTRAINT cnstr_client_init_acc_pk PRIMARY KEY (id);


--
-- Name: realm_default_groups con_group_id_def_groups; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_default_groups
    ADD CONSTRAINT con_group_id_def_groups UNIQUE (group_id);


--
-- Name: broker_link constr_broker_link_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.broker_link
    ADD CONSTRAINT constr_broker_link_pk PRIMARY KEY (identity_provider, user_id);


--
-- Name: component_config constr_component_config_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.component_config
    ADD CONSTRAINT constr_component_config_pk PRIMARY KEY (id);


--
-- Name: component constr_component_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.component
    ADD CONSTRAINT constr_component_pk PRIMARY KEY (id);


--
-- Name: fed_user_required_action constr_fed_required_action; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.fed_user_required_action
    ADD CONSTRAINT constr_fed_required_action PRIMARY KEY (required_action, user_id);


--
-- Name: fed_user_attribute constr_fed_user_attr_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.fed_user_attribute
    ADD CONSTRAINT constr_fed_user_attr_pk PRIMARY KEY (id);


--
-- Name: fed_user_consent constr_fed_user_consent_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.fed_user_consent
    ADD CONSTRAINT constr_fed_user_consent_pk PRIMARY KEY (id);


--
-- Name: fed_user_credential constr_fed_user_cred_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.fed_user_credential
    ADD CONSTRAINT constr_fed_user_cred_pk PRIMARY KEY (id);


--
-- Name: fed_user_group_membership constr_fed_user_group; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.fed_user_group_membership
    ADD CONSTRAINT constr_fed_user_group PRIMARY KEY (group_id, user_id);


--
-- Name: fed_user_role_mapping constr_fed_user_role; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.fed_user_role_mapping
    ADD CONSTRAINT constr_fed_user_role PRIMARY KEY (role_id, user_id);


--
-- Name: federated_user constr_federated_user; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.federated_user
    ADD CONSTRAINT constr_federated_user PRIMARY KEY (id);


--
-- Name: realm_default_groups constr_realm_default_groups; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_default_groups
    ADD CONSTRAINT constr_realm_default_groups PRIMARY KEY (realm_id, group_id);


--
-- Name: realm_enabled_event_types constr_realm_enabl_event_types; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_enabled_event_types
    ADD CONSTRAINT constr_realm_enabl_event_types PRIMARY KEY (realm_id, value);


--
-- Name: realm_events_listeners constr_realm_events_listeners; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_events_listeners
    ADD CONSTRAINT constr_realm_events_listeners PRIMARY KEY (realm_id, value);


--
-- Name: realm_supported_locales constr_realm_supported_locales; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_supported_locales
    ADD CONSTRAINT constr_realm_supported_locales PRIMARY KEY (realm_id, value);


--
-- Name: identity_provider constraint_2b; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.identity_provider
    ADD CONSTRAINT constraint_2b PRIMARY KEY (internal_id);


--
-- Name: client_attributes constraint_3c; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_attributes
    ADD CONSTRAINT constraint_3c PRIMARY KEY (client_id, name);


--
-- Name: event_entity constraint_4; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.event_entity
    ADD CONSTRAINT constraint_4 PRIMARY KEY (id);


--
-- Name: federated_identity constraint_40; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.federated_identity
    ADD CONSTRAINT constraint_40 PRIMARY KEY (identity_provider, user_id);


--
-- Name: realm constraint_4a; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm
    ADD CONSTRAINT constraint_4a PRIMARY KEY (id);


--
-- Name: user_federation_provider constraint_5c; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_provider
    ADD CONSTRAINT constraint_5c PRIMARY KEY (id);


--
-- Name: client constraint_7; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT constraint_7 PRIMARY KEY (id);


--
-- Name: scope_mapping constraint_81; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.scope_mapping
    ADD CONSTRAINT constraint_81 PRIMARY KEY (client_id, role_id);


--
-- Name: client_node_registrations constraint_84; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_node_registrations
    ADD CONSTRAINT constraint_84 PRIMARY KEY (client_id, name);


--
-- Name: realm_attribute constraint_9; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_attribute
    ADD CONSTRAINT constraint_9 PRIMARY KEY (name, realm_id);


--
-- Name: realm_required_credential constraint_92; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_required_credential
    ADD CONSTRAINT constraint_92 PRIMARY KEY (realm_id, type);


--
-- Name: keycloak_role constraint_a; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.keycloak_role
    ADD CONSTRAINT constraint_a PRIMARY KEY (id);


--
-- Name: admin_event_entity constraint_admin_event_entity; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.admin_event_entity
    ADD CONSTRAINT constraint_admin_event_entity PRIMARY KEY (id);


--
-- Name: authenticator_config_entry constraint_auth_cfg_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.authenticator_config_entry
    ADD CONSTRAINT constraint_auth_cfg_pk PRIMARY KEY (authenticator_id, name);


--
-- Name: authentication_execution constraint_auth_exec_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.authentication_execution
    ADD CONSTRAINT constraint_auth_exec_pk PRIMARY KEY (id);


--
-- Name: authentication_flow constraint_auth_flow_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.authentication_flow
    ADD CONSTRAINT constraint_auth_flow_pk PRIMARY KEY (id);


--
-- Name: authenticator_config constraint_auth_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.authenticator_config
    ADD CONSTRAINT constraint_auth_pk PRIMARY KEY (id);


--
-- Name: user_role_mapping constraint_c; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_role_mapping
    ADD CONSTRAINT constraint_c PRIMARY KEY (role_id, user_id);


--
-- Name: composite_role constraint_composite_role; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.composite_role
    ADD CONSTRAINT constraint_composite_role PRIMARY KEY (composite, child_role);


--
-- Name: identity_provider_config constraint_d; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.identity_provider_config
    ADD CONSTRAINT constraint_d PRIMARY KEY (identity_provider_id, name);


--
-- Name: policy_config constraint_dpc; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.policy_config
    ADD CONSTRAINT constraint_dpc PRIMARY KEY (policy_id, name);


--
-- Name: realm_smtp_config constraint_e; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_smtp_config
    ADD CONSTRAINT constraint_e PRIMARY KEY (realm_id, name);


--
-- Name: credential constraint_f; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.credential
    ADD CONSTRAINT constraint_f PRIMARY KEY (id);


--
-- Name: user_federation_config constraint_f9; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_config
    ADD CONSTRAINT constraint_f9 PRIMARY KEY (user_federation_provider_id, name);


--
-- Name: resource_server_perm_ticket constraint_fapmt; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_perm_ticket
    ADD CONSTRAINT constraint_fapmt PRIMARY KEY (id);


--
-- Name: resource_server_resource constraint_farsr; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_resource
    ADD CONSTRAINT constraint_farsr PRIMARY KEY (id);


--
-- Name: resource_server_policy constraint_farsrp; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_policy
    ADD CONSTRAINT constraint_farsrp PRIMARY KEY (id);


--
-- Name: associated_policy constraint_farsrpap; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.associated_policy
    ADD CONSTRAINT constraint_farsrpap PRIMARY KEY (policy_id, associated_policy_id);


--
-- Name: resource_policy constraint_farsrpp; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_policy
    ADD CONSTRAINT constraint_farsrpp PRIMARY KEY (resource_id, policy_id);


--
-- Name: resource_server_scope constraint_farsrs; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_scope
    ADD CONSTRAINT constraint_farsrs PRIMARY KEY (id);


--
-- Name: resource_scope constraint_farsrsp; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_scope
    ADD CONSTRAINT constraint_farsrsp PRIMARY KEY (resource_id, scope_id);


--
-- Name: scope_policy constraint_farsrsps; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.scope_policy
    ADD CONSTRAINT constraint_farsrsps PRIMARY KEY (scope_id, policy_id);


--
-- Name: user_entity constraint_fb; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_entity
    ADD CONSTRAINT constraint_fb PRIMARY KEY (id);


--
-- Name: user_federation_mapper_config constraint_fedmapper_cfg_pm; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_mapper_config
    ADD CONSTRAINT constraint_fedmapper_cfg_pm PRIMARY KEY (user_federation_mapper_id, name);


--
-- Name: user_federation_mapper constraint_fedmapperpm; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_mapper
    ADD CONSTRAINT constraint_fedmapperpm PRIMARY KEY (id);


--
-- Name: fed_user_consent_cl_scope constraint_fgrntcsnt_clsc_pm; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.fed_user_consent_cl_scope
    ADD CONSTRAINT constraint_fgrntcsnt_clsc_pm PRIMARY KEY (user_consent_id, scope_id);


--
-- Name: user_consent_client_scope constraint_grntcsnt_clsc_pm; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_consent_client_scope
    ADD CONSTRAINT constraint_grntcsnt_clsc_pm PRIMARY KEY (user_consent_id, scope_id);


--
-- Name: user_consent constraint_grntcsnt_pm; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_consent
    ADD CONSTRAINT constraint_grntcsnt_pm PRIMARY KEY (id);


--
-- Name: keycloak_group constraint_group; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.keycloak_group
    ADD CONSTRAINT constraint_group PRIMARY KEY (id);


--
-- Name: group_attribute constraint_group_attribute_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.group_attribute
    ADD CONSTRAINT constraint_group_attribute_pk PRIMARY KEY (id);


--
-- Name: group_role_mapping constraint_group_role; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.group_role_mapping
    ADD CONSTRAINT constraint_group_role PRIMARY KEY (role_id, group_id);


--
-- Name: identity_provider_mapper constraint_idpm; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.identity_provider_mapper
    ADD CONSTRAINT constraint_idpm PRIMARY KEY (id);


--
-- Name: idp_mapper_config constraint_idpmconfig; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.idp_mapper_config
    ADD CONSTRAINT constraint_idpmconfig PRIMARY KEY (idp_mapper_id, name);


--
-- Name: jgroups_ping constraint_jgroups_ping; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.jgroups_ping
    ADD CONSTRAINT constraint_jgroups_ping PRIMARY KEY (address);


--
-- Name: migration_model constraint_migmod; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.migration_model
    ADD CONSTRAINT constraint_migmod PRIMARY KEY (id);


--
-- Name: offline_client_session constraint_offl_cl_ses_pk3; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.offline_client_session
    ADD CONSTRAINT constraint_offl_cl_ses_pk3 PRIMARY KEY (user_session_id, client_id, client_storage_provider, external_client_id, offline_flag);


--
-- Name: offline_user_session constraint_offl_us_ses_pk2; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.offline_user_session
    ADD CONSTRAINT constraint_offl_us_ses_pk2 PRIMARY KEY (user_session_id, offline_flag);


--
-- Name: org_invitation constraint_org_invitation; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.org_invitation
    ADD CONSTRAINT constraint_org_invitation PRIMARY KEY (id);


--
-- Name: protocol_mapper constraint_pcm; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.protocol_mapper
    ADD CONSTRAINT constraint_pcm PRIMARY KEY (id);


--
-- Name: protocol_mapper_config constraint_pmconfig; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.protocol_mapper_config
    ADD CONSTRAINT constraint_pmconfig PRIMARY KEY (protocol_mapper_id, name);


--
-- Name: redirect_uris constraint_redirect_uris; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.redirect_uris
    ADD CONSTRAINT constraint_redirect_uris PRIMARY KEY (client_id, value);


--
-- Name: required_action_config constraint_req_act_cfg_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.required_action_config
    ADD CONSTRAINT constraint_req_act_cfg_pk PRIMARY KEY (required_action_id, name);


--
-- Name: required_action_provider constraint_req_act_prv_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.required_action_provider
    ADD CONSTRAINT constraint_req_act_prv_pk PRIMARY KEY (id);


--
-- Name: user_required_action constraint_required_action; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_required_action
    ADD CONSTRAINT constraint_required_action PRIMARY KEY (required_action, user_id);


--
-- Name: resource_uris constraint_resour_uris_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_uris
    ADD CONSTRAINT constraint_resour_uris_pk PRIMARY KEY (resource_id, value);


--
-- Name: role_attribute constraint_role_attribute_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.role_attribute
    ADD CONSTRAINT constraint_role_attribute_pk PRIMARY KEY (id);


--
-- Name: revoked_token constraint_rt; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.revoked_token
    ADD CONSTRAINT constraint_rt PRIMARY KEY (id);


--
-- Name: user_attribute constraint_user_attribute_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_attribute
    ADD CONSTRAINT constraint_user_attribute_pk PRIMARY KEY (id);


--
-- Name: user_group_membership constraint_user_group; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_group_membership
    ADD CONSTRAINT constraint_user_group PRIMARY KEY (group_id, user_id);


--
-- Name: web_origins constraint_web_origins; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.web_origins
    ADD CONSTRAINT constraint_web_origins PRIMARY KEY (client_id, value);


--
-- Name: databasechangeloglock databasechangeloglock_pkey; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.databasechangeloglock
    ADD CONSTRAINT databasechangeloglock_pkey PRIMARY KEY (id);


--
-- Name: client_scope_attributes pk_cl_tmpl_attr; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_scope_attributes
    ADD CONSTRAINT pk_cl_tmpl_attr PRIMARY KEY (scope_id, name);


--
-- Name: client_scope pk_cli_template; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_scope
    ADD CONSTRAINT pk_cli_template PRIMARY KEY (id);


--
-- Name: resource_server pk_resource_server; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server
    ADD CONSTRAINT pk_resource_server PRIMARY KEY (id);


--
-- Name: client_scope_role_mapping pk_template_scope; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_scope_role_mapping
    ADD CONSTRAINT pk_template_scope PRIMARY KEY (scope_id, role_id);


--
-- Name: workflow_state pk_workflow_state; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.workflow_state
    ADD CONSTRAINT pk_workflow_state PRIMARY KEY (execution_id);


--
-- Name: default_client_scope r_def_cli_scope_bind; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.default_client_scope
    ADD CONSTRAINT r_def_cli_scope_bind PRIMARY KEY (realm_id, scope_id);


--
-- Name: realm_localizations realm_localizations_pkey; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_localizations
    ADD CONSTRAINT realm_localizations_pkey PRIMARY KEY (realm_id, locale);


--
-- Name: resource_attribute res_attr_pk; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_attribute
    ADD CONSTRAINT res_attr_pk PRIMARY KEY (id);


--
-- Name: keycloak_group sibling_names; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.keycloak_group
    ADD CONSTRAINT sibling_names UNIQUE (realm_id, parent_group, name);


--
-- Name: identity_provider uk_2daelwnibji49avxsrtuf6xj33; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.identity_provider
    ADD CONSTRAINT uk_2daelwnibji49avxsrtuf6xj33 UNIQUE (provider_alias, realm_id);


--
-- Name: client uk_b71cjlbenv945rb6gcon438at; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT uk_b71cjlbenv945rb6gcon438at UNIQUE (realm_id, client_id);


--
-- Name: client_scope uk_cli_scope; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_scope
    ADD CONSTRAINT uk_cli_scope UNIQUE (realm_id, name);


--
-- Name: user_entity uk_dykn684sl8up1crfei6eckhd7; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_entity
    ADD CONSTRAINT uk_dykn684sl8up1crfei6eckhd7 UNIQUE (realm_id, email_constraint);


--
-- Name: user_consent uk_external_consent; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_consent
    ADD CONSTRAINT uk_external_consent UNIQUE (client_storage_provider, external_client_id, user_id);


--
-- Name: resource_server_resource uk_frsr6t700s9v50bu18ws5ha6; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_resource
    ADD CONSTRAINT uk_frsr6t700s9v50bu18ws5ha6 UNIQUE (name, owner, resource_server_id);


--
-- Name: resource_server_perm_ticket uk_frsr6t700s9v50bu18ws5pmt; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_perm_ticket
    ADD CONSTRAINT uk_frsr6t700s9v50bu18ws5pmt UNIQUE (owner, requester, resource_server_id, resource_id, scope_id);


--
-- Name: resource_server_policy uk_frsrpt700s9v50bu18ws5ha6; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_policy
    ADD CONSTRAINT uk_frsrpt700s9v50bu18ws5ha6 UNIQUE (name, resource_server_id);


--
-- Name: resource_server_scope uk_frsrst700s9v50bu18ws5ha6; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_scope
    ADD CONSTRAINT uk_frsrst700s9v50bu18ws5ha6 UNIQUE (name, resource_server_id);


--
-- Name: user_consent uk_local_consent; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_consent
    ADD CONSTRAINT uk_local_consent UNIQUE (client_id, user_id);


--
-- Name: migration_model uk_migration_update_time; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.migration_model
    ADD CONSTRAINT uk_migration_update_time UNIQUE (update_time);


--
-- Name: migration_model uk_migration_version; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.migration_model
    ADD CONSTRAINT uk_migration_version UNIQUE (version);


--
-- Name: org uk_org_alias; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.org
    ADD CONSTRAINT uk_org_alias UNIQUE (realm_id, alias);


--
-- Name: org uk_org_group; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.org
    ADD CONSTRAINT uk_org_group UNIQUE (group_id);


--
-- Name: org_invitation uk_org_invitation_email; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.org_invitation
    ADD CONSTRAINT uk_org_invitation_email UNIQUE (organization_id, email);


--
-- Name: org uk_org_name; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.org
    ADD CONSTRAINT uk_org_name UNIQUE (realm_id, name);


--
-- Name: realm uk_orvsdmla56612eaefiq6wl5oi; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm
    ADD CONSTRAINT uk_orvsdmla56612eaefiq6wl5oi UNIQUE (name);


--
-- Name: user_entity uk_ru8tt6t700s9v50bu18ws5ha6; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_entity
    ADD CONSTRAINT uk_ru8tt6t700s9v50bu18ws5ha6 UNIQUE (realm_id, username);


--
-- Name: workflow_state uq_workflow_resource; Type: CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.workflow_state
    ADD CONSTRAINT uq_workflow_resource UNIQUE (workflow_id, resource_id);


--
-- Name: fed_user_attr_long_values; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX fed_user_attr_long_values ON public.fed_user_attribute USING btree (long_value_hash, name);


--
-- Name: fed_user_attr_long_values_lower_case; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX fed_user_attr_long_values_lower_case ON public.fed_user_attribute USING btree (long_value_hash_lower_case, name);


--
-- Name: idx_admin_event_time; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_admin_event_time ON public.admin_event_entity USING btree (realm_id, admin_event_time);


--
-- Name: idx_assoc_pol_assoc_pol_id; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_assoc_pol_assoc_pol_id ON public.associated_policy USING btree (associated_policy_id);


--
-- Name: idx_auth_config_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_auth_config_realm ON public.authenticator_config USING btree (realm_id);


--
-- Name: idx_auth_exec_flow; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_auth_exec_flow ON public.authentication_execution USING btree (flow_id);


--
-- Name: idx_auth_exec_realm_flow; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_auth_exec_realm_flow ON public.authentication_execution USING btree (realm_id, flow_id);


--
-- Name: idx_auth_flow_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_auth_flow_realm ON public.authentication_flow USING btree (realm_id);


--
-- Name: idx_cl_clscope; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_cl_clscope ON public.client_scope_client USING btree (scope_id);


--
-- Name: idx_client_att_by_name_value; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_client_att_by_name_value ON public.client_attributes USING btree (name, substr(value, 1, 255));


--
-- Name: idx_client_id; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_client_id ON public.client USING btree (client_id);


--
-- Name: idx_client_init_acc_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_client_init_acc_realm ON public.client_initial_access USING btree (realm_id);


--
-- Name: idx_clscope_attrs; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_clscope_attrs ON public.client_scope_attributes USING btree (scope_id);


--
-- Name: idx_clscope_cl; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_clscope_cl ON public.client_scope_client USING btree (client_id);


--
-- Name: idx_clscope_protmap; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_clscope_protmap ON public.protocol_mapper USING btree (client_scope_id);


--
-- Name: idx_clscope_role; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_clscope_role ON public.client_scope_role_mapping USING btree (scope_id);


--
-- Name: idx_compo_config_compo; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_compo_config_compo ON public.component_config USING btree (component_id);


--
-- Name: idx_component_provider_type; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_component_provider_type ON public.component USING btree (provider_type);


--
-- Name: idx_component_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_component_realm ON public.component USING btree (realm_id);


--
-- Name: idx_composite; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_composite ON public.composite_role USING btree (composite);


--
-- Name: idx_composite_child; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_composite_child ON public.composite_role USING btree (child_role);


--
-- Name: idx_defcls_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_defcls_realm ON public.default_client_scope USING btree (realm_id);


--
-- Name: idx_defcls_scope; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_defcls_scope ON public.default_client_scope USING btree (scope_id);


--
-- Name: idx_event_entity_user_id_type; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_event_entity_user_id_type ON public.event_entity USING btree (user_id, type, event_time);


--
-- Name: idx_event_time; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_event_time ON public.event_entity USING btree (realm_id, event_time);


--
-- Name: idx_fedidentity_feduser; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fedidentity_feduser ON public.federated_identity USING btree (federated_user_id);


--
-- Name: idx_fedidentity_user; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fedidentity_user ON public.federated_identity USING btree (user_id);


--
-- Name: idx_fu_attribute; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_attribute ON public.fed_user_attribute USING btree (user_id, realm_id, name);


--
-- Name: idx_fu_cnsnt_ext; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_cnsnt_ext ON public.fed_user_consent USING btree (user_id, client_storage_provider, external_client_id);


--
-- Name: idx_fu_consent; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_consent ON public.fed_user_consent USING btree (user_id, client_id);


--
-- Name: idx_fu_consent_ru; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_consent_ru ON public.fed_user_consent USING btree (realm_id, user_id);


--
-- Name: idx_fu_credential; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_credential ON public.fed_user_credential USING btree (user_id, type);


--
-- Name: idx_fu_credential_ru; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_credential_ru ON public.fed_user_credential USING btree (realm_id, user_id);


--
-- Name: idx_fu_group_membership; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_group_membership ON public.fed_user_group_membership USING btree (user_id, group_id);


--
-- Name: idx_fu_group_membership_ru; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_group_membership_ru ON public.fed_user_group_membership USING btree (realm_id, user_id);


--
-- Name: idx_fu_required_action; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_required_action ON public.fed_user_required_action USING btree (user_id, required_action);


--
-- Name: idx_fu_required_action_ru; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_required_action_ru ON public.fed_user_required_action USING btree (realm_id, user_id);


--
-- Name: idx_fu_role_mapping; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_role_mapping ON public.fed_user_role_mapping USING btree (user_id, role_id);


--
-- Name: idx_fu_role_mapping_ru; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_fu_role_mapping_ru ON public.fed_user_role_mapping USING btree (realm_id, user_id);


--
-- Name: idx_group_att_by_name_value; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_group_att_by_name_value ON public.group_attribute USING btree (name, ((value)::character varying(250)));


--
-- Name: idx_group_attr_group; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_group_attr_group ON public.group_attribute USING btree (group_id);


--
-- Name: idx_group_role_mapp_group; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_group_role_mapp_group ON public.group_role_mapping USING btree (group_id);


--
-- Name: idx_id_prov_mapp_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_id_prov_mapp_realm ON public.identity_provider_mapper USING btree (realm_id);


--
-- Name: idx_ident_prov_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_ident_prov_realm ON public.identity_provider USING btree (realm_id);


--
-- Name: idx_idp_for_login; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_idp_for_login ON public.identity_provider USING btree (realm_id, enabled, link_only, hide_on_login, organization_id);


--
-- Name: idx_idp_realm_org; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_idp_realm_org ON public.identity_provider USING btree (realm_id, organization_id);


--
-- Name: idx_keycloak_role_client; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_keycloak_role_client ON public.keycloak_role USING btree (client);


--
-- Name: idx_keycloak_role_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_keycloak_role_realm ON public.keycloak_role USING btree (realm);


--
-- Name: idx_offline_css_by_client; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_offline_css_by_client ON public.offline_client_session USING btree (client_id, offline_flag) WHERE ((client_id)::text <> 'external'::text);


--
-- Name: idx_offline_css_by_client_storage_provider; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_offline_css_by_client_storage_provider ON public.offline_client_session USING btree (client_storage_provider, external_client_id, offline_flag) WHERE ((client_storage_provider)::text <> 'internal'::text);


--
-- Name: idx_offline_uss_by_broker_session_id; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_offline_uss_by_broker_session_id ON public.offline_user_session USING btree (broker_session_id, realm_id);


--
-- Name: idx_offline_uss_by_user; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_offline_uss_by_user ON public.offline_user_session USING btree (user_id, realm_id, offline_flag);


--
-- Name: idx_org_domain_org_id; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_org_domain_org_id ON public.org_domain USING btree (org_id);


--
-- Name: idx_org_invitation_email; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_org_invitation_email ON public.org_invitation USING btree (email);


--
-- Name: idx_org_invitation_expires; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_org_invitation_expires ON public.org_invitation USING btree (expires_at);


--
-- Name: idx_org_invitation_org_id; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_org_invitation_org_id ON public.org_invitation USING btree (organization_id);


--
-- Name: idx_perm_ticket_owner; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_perm_ticket_owner ON public.resource_server_perm_ticket USING btree (owner);


--
-- Name: idx_perm_ticket_requester; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_perm_ticket_requester ON public.resource_server_perm_ticket USING btree (requester);


--
-- Name: idx_protocol_mapper_client; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_protocol_mapper_client ON public.protocol_mapper USING btree (client_id);


--
-- Name: idx_realm_attr_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_realm_attr_realm ON public.realm_attribute USING btree (realm_id);


--
-- Name: idx_realm_clscope; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_realm_clscope ON public.client_scope USING btree (realm_id);


--
-- Name: idx_realm_def_grp_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_realm_def_grp_realm ON public.realm_default_groups USING btree (realm_id);


--
-- Name: idx_realm_evt_list_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_realm_evt_list_realm ON public.realm_events_listeners USING btree (realm_id);


--
-- Name: idx_realm_evt_types_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_realm_evt_types_realm ON public.realm_enabled_event_types USING btree (realm_id);


--
-- Name: idx_realm_master_adm_cli; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_realm_master_adm_cli ON public.realm USING btree (master_admin_client);


--
-- Name: idx_realm_supp_local_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_realm_supp_local_realm ON public.realm_supported_locales USING btree (realm_id);


--
-- Name: idx_redir_uri_client; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_redir_uri_client ON public.redirect_uris USING btree (client_id);


--
-- Name: idx_req_act_prov_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_req_act_prov_realm ON public.required_action_provider USING btree (realm_id);


--
-- Name: idx_res_policy_policy; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_res_policy_policy ON public.resource_policy USING btree (policy_id);


--
-- Name: idx_res_scope_scope; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_res_scope_scope ON public.resource_scope USING btree (scope_id);


--
-- Name: idx_res_serv_pol_res_serv; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_res_serv_pol_res_serv ON public.resource_server_policy USING btree (resource_server_id);


--
-- Name: idx_res_srv_res_res_srv; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_res_srv_res_res_srv ON public.resource_server_resource USING btree (resource_server_id);


--
-- Name: idx_res_srv_scope_res_srv; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_res_srv_scope_res_srv ON public.resource_server_scope USING btree (resource_server_id);


--
-- Name: idx_rev_token_on_expire; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_rev_token_on_expire ON public.revoked_token USING btree (expire);


--
-- Name: idx_role_attribute; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_role_attribute ON public.role_attribute USING btree (role_id);


--
-- Name: idx_role_clscope; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_role_clscope ON public.client_scope_role_mapping USING btree (role_id);


--
-- Name: idx_scope_mapping_role; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_scope_mapping_role ON public.scope_mapping USING btree (role_id);


--
-- Name: idx_scope_policy_policy; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_scope_policy_policy ON public.scope_policy USING btree (policy_id);


--
-- Name: idx_update_time; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_update_time ON public.migration_model USING btree (update_time);


--
-- Name: idx_usconsent_clscope; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_usconsent_clscope ON public.user_consent_client_scope USING btree (user_consent_id);


--
-- Name: idx_usconsent_scope_id; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_usconsent_scope_id ON public.user_consent_client_scope USING btree (scope_id);


--
-- Name: idx_user_attribute; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_attribute ON public.user_attribute USING btree (user_id);


--
-- Name: idx_user_attribute_name; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_attribute_name ON public.user_attribute USING btree (name, value);


--
-- Name: idx_user_consent; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_consent ON public.user_consent USING btree (user_id);


--
-- Name: idx_user_credential; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_credential ON public.credential USING btree (user_id);


--
-- Name: idx_user_email; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_email ON public.user_entity USING btree (email);


--
-- Name: idx_user_group_mapping; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_group_mapping ON public.user_group_membership USING btree (user_id);


--
-- Name: idx_user_reqactions; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_reqactions ON public.user_required_action USING btree (user_id);


--
-- Name: idx_user_role_mapping; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_role_mapping ON public.user_role_mapping USING btree (user_id);


--
-- Name: idx_user_service_account; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_service_account ON public.user_entity USING btree (realm_id, service_account_client_link);


--
-- Name: idx_user_session_expiration_created; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_session_expiration_created ON public.offline_user_session USING btree (realm_id, offline_flag, remember_me, created_on, user_session_id, user_id);


--
-- Name: idx_user_session_expiration_last_refresh; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_user_session_expiration_last_refresh ON public.offline_user_session USING btree (realm_id, offline_flag, remember_me, last_session_refresh, user_session_id, user_id);


--
-- Name: idx_usr_fed_map_fed_prv; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_usr_fed_map_fed_prv ON public.user_federation_mapper USING btree (federation_provider_id);


--
-- Name: idx_usr_fed_map_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_usr_fed_map_realm ON public.user_federation_mapper USING btree (realm_id);


--
-- Name: idx_usr_fed_prv_realm; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_usr_fed_prv_realm ON public.user_federation_provider USING btree (realm_id);


--
-- Name: idx_web_orig_client; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_web_orig_client ON public.web_origins USING btree (client_id);


--
-- Name: idx_workflow_state_provider; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_workflow_state_provider ON public.workflow_state USING btree (resource_id);


--
-- Name: idx_workflow_state_step; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX idx_workflow_state_step ON public.workflow_state USING btree (workflow_id, scheduled_step_id);


--
-- Name: user_attr_long_values; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX user_attr_long_values ON public.user_attribute USING btree (long_value_hash, name);


--
-- Name: user_attr_long_values_lower_case; Type: INDEX; Schema: public; Owner: csfeer
--

CREATE INDEX user_attr_long_values_lower_case ON public.user_attribute USING btree (long_value_hash_lower_case, name);


--
-- Name: identity_provider fk2b4ebc52ae5c3b34; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.identity_provider
    ADD CONSTRAINT fk2b4ebc52ae5c3b34 FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: client_attributes fk3c47c64beacca966; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_attributes
    ADD CONSTRAINT fk3c47c64beacca966 FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: federated_identity fk404288b92ef007a6; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.federated_identity
    ADD CONSTRAINT fk404288b92ef007a6 FOREIGN KEY (user_id) REFERENCES public.user_entity(id);


--
-- Name: client_node_registrations fk4129723ba992f594; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_node_registrations
    ADD CONSTRAINT fk4129723ba992f594 FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: redirect_uris fk_1burs8pb4ouj97h5wuppahv9f; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.redirect_uris
    ADD CONSTRAINT fk_1burs8pb4ouj97h5wuppahv9f FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: user_federation_provider fk_1fj32f6ptolw2qy60cd8n01e8; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_provider
    ADD CONSTRAINT fk_1fj32f6ptolw2qy60cd8n01e8 FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: realm_required_credential fk_5hg65lybevavkqfki3kponh9v; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_required_credential
    ADD CONSTRAINT fk_5hg65lybevavkqfki3kponh9v FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: resource_attribute fk_5hrm2vlf9ql5fu022kqepovbr; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_attribute
    ADD CONSTRAINT fk_5hrm2vlf9ql5fu022kqepovbr FOREIGN KEY (resource_id) REFERENCES public.resource_server_resource(id);


--
-- Name: user_attribute fk_5hrm2vlf9ql5fu043kqepovbr; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_attribute
    ADD CONSTRAINT fk_5hrm2vlf9ql5fu043kqepovbr FOREIGN KEY (user_id) REFERENCES public.user_entity(id);


--
-- Name: user_required_action fk_6qj3w1jw9cvafhe19bwsiuvmd; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_required_action
    ADD CONSTRAINT fk_6qj3w1jw9cvafhe19bwsiuvmd FOREIGN KEY (user_id) REFERENCES public.user_entity(id);


--
-- Name: keycloak_role fk_6vyqfe4cn4wlq8r6kt5vdsj5c; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.keycloak_role
    ADD CONSTRAINT fk_6vyqfe4cn4wlq8r6kt5vdsj5c FOREIGN KEY (realm) REFERENCES public.realm(id);


--
-- Name: realm_smtp_config fk_70ej8xdxgxd0b9hh6180irr0o; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_smtp_config
    ADD CONSTRAINT fk_70ej8xdxgxd0b9hh6180irr0o FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: realm_attribute fk_8shxd6l3e9atqukacxgpffptw; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_attribute
    ADD CONSTRAINT fk_8shxd6l3e9atqukacxgpffptw FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: composite_role fk_a63wvekftu8jo1pnj81e7mce2; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.composite_role
    ADD CONSTRAINT fk_a63wvekftu8jo1pnj81e7mce2 FOREIGN KEY (composite) REFERENCES public.keycloak_role(id);


--
-- Name: authentication_execution fk_auth_exec_flow; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.authentication_execution
    ADD CONSTRAINT fk_auth_exec_flow FOREIGN KEY (flow_id) REFERENCES public.authentication_flow(id);


--
-- Name: authentication_execution fk_auth_exec_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.authentication_execution
    ADD CONSTRAINT fk_auth_exec_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: authentication_flow fk_auth_flow_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.authentication_flow
    ADD CONSTRAINT fk_auth_flow_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: authenticator_config fk_auth_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.authenticator_config
    ADD CONSTRAINT fk_auth_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: user_role_mapping fk_c4fqv34p1mbylloxang7b1q3l; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_role_mapping
    ADD CONSTRAINT fk_c4fqv34p1mbylloxang7b1q3l FOREIGN KEY (user_id) REFERENCES public.user_entity(id);


--
-- Name: client_scope_attributes fk_cl_scope_attr_scope; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_scope_attributes
    ADD CONSTRAINT fk_cl_scope_attr_scope FOREIGN KEY (scope_id) REFERENCES public.client_scope(id);


--
-- Name: client_scope_role_mapping fk_cl_scope_rm_scope; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_scope_role_mapping
    ADD CONSTRAINT fk_cl_scope_rm_scope FOREIGN KEY (scope_id) REFERENCES public.client_scope(id);


--
-- Name: protocol_mapper fk_cli_scope_mapper; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.protocol_mapper
    ADD CONSTRAINT fk_cli_scope_mapper FOREIGN KEY (client_scope_id) REFERENCES public.client_scope(id);


--
-- Name: client_initial_access fk_client_init_acc_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.client_initial_access
    ADD CONSTRAINT fk_client_init_acc_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: component_config fk_component_config; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.component_config
    ADD CONSTRAINT fk_component_config FOREIGN KEY (component_id) REFERENCES public.component(id);


--
-- Name: component fk_component_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.component
    ADD CONSTRAINT fk_component_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: realm_default_groups fk_def_groups_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_default_groups
    ADD CONSTRAINT fk_def_groups_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: user_federation_mapper_config fk_fedmapper_cfg; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_mapper_config
    ADD CONSTRAINT fk_fedmapper_cfg FOREIGN KEY (user_federation_mapper_id) REFERENCES public.user_federation_mapper(id);


--
-- Name: user_federation_mapper fk_fedmapperpm_fedprv; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_mapper
    ADD CONSTRAINT fk_fedmapperpm_fedprv FOREIGN KEY (federation_provider_id) REFERENCES public.user_federation_provider(id);


--
-- Name: user_federation_mapper fk_fedmapperpm_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_mapper
    ADD CONSTRAINT fk_fedmapperpm_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: associated_policy fk_frsr5s213xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.associated_policy
    ADD CONSTRAINT fk_frsr5s213xcx4wnkog82ssrfy FOREIGN KEY (associated_policy_id) REFERENCES public.resource_server_policy(id);


--
-- Name: scope_policy fk_frsrasp13xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.scope_policy
    ADD CONSTRAINT fk_frsrasp13xcx4wnkog82ssrfy FOREIGN KEY (policy_id) REFERENCES public.resource_server_policy(id);


--
-- Name: resource_server_perm_ticket fk_frsrho213xcx4wnkog82sspmt; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_perm_ticket
    ADD CONSTRAINT fk_frsrho213xcx4wnkog82sspmt FOREIGN KEY (resource_server_id) REFERENCES public.resource_server(id);


--
-- Name: resource_server_resource fk_frsrho213xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_resource
    ADD CONSTRAINT fk_frsrho213xcx4wnkog82ssrfy FOREIGN KEY (resource_server_id) REFERENCES public.resource_server(id);


--
-- Name: resource_server_perm_ticket fk_frsrho213xcx4wnkog83sspmt; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_perm_ticket
    ADD CONSTRAINT fk_frsrho213xcx4wnkog83sspmt FOREIGN KEY (resource_id) REFERENCES public.resource_server_resource(id);


--
-- Name: resource_server_perm_ticket fk_frsrho213xcx4wnkog84sspmt; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_perm_ticket
    ADD CONSTRAINT fk_frsrho213xcx4wnkog84sspmt FOREIGN KEY (scope_id) REFERENCES public.resource_server_scope(id);


--
-- Name: associated_policy fk_frsrpas14xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.associated_policy
    ADD CONSTRAINT fk_frsrpas14xcx4wnkog82ssrfy FOREIGN KEY (policy_id) REFERENCES public.resource_server_policy(id);


--
-- Name: scope_policy fk_frsrpass3xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.scope_policy
    ADD CONSTRAINT fk_frsrpass3xcx4wnkog82ssrfy FOREIGN KEY (scope_id) REFERENCES public.resource_server_scope(id);


--
-- Name: resource_server_perm_ticket fk_frsrpo2128cx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_perm_ticket
    ADD CONSTRAINT fk_frsrpo2128cx4wnkog82ssrfy FOREIGN KEY (policy_id) REFERENCES public.resource_server_policy(id);


--
-- Name: resource_server_policy fk_frsrpo213xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_policy
    ADD CONSTRAINT fk_frsrpo213xcx4wnkog82ssrfy FOREIGN KEY (resource_server_id) REFERENCES public.resource_server(id);


--
-- Name: resource_scope fk_frsrpos13xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_scope
    ADD CONSTRAINT fk_frsrpos13xcx4wnkog82ssrfy FOREIGN KEY (resource_id) REFERENCES public.resource_server_resource(id);


--
-- Name: resource_policy fk_frsrpos53xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_policy
    ADD CONSTRAINT fk_frsrpos53xcx4wnkog82ssrfy FOREIGN KEY (resource_id) REFERENCES public.resource_server_resource(id);


--
-- Name: resource_policy fk_frsrpp213xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_policy
    ADD CONSTRAINT fk_frsrpp213xcx4wnkog82ssrfy FOREIGN KEY (policy_id) REFERENCES public.resource_server_policy(id);


--
-- Name: resource_scope fk_frsrps213xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_scope
    ADD CONSTRAINT fk_frsrps213xcx4wnkog82ssrfy FOREIGN KEY (scope_id) REFERENCES public.resource_server_scope(id);


--
-- Name: resource_server_scope fk_frsrso213xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_server_scope
    ADD CONSTRAINT fk_frsrso213xcx4wnkog82ssrfy FOREIGN KEY (resource_server_id) REFERENCES public.resource_server(id);


--
-- Name: composite_role fk_gr7thllb9lu8q4vqa4524jjy8; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.composite_role
    ADD CONSTRAINT fk_gr7thllb9lu8q4vqa4524jjy8 FOREIGN KEY (child_role) REFERENCES public.keycloak_role(id);


--
-- Name: user_consent_client_scope fk_grntcsnt_clsc_usc; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_consent_client_scope
    ADD CONSTRAINT fk_grntcsnt_clsc_usc FOREIGN KEY (user_consent_id) REFERENCES public.user_consent(id);


--
-- Name: user_consent fk_grntcsnt_user; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_consent
    ADD CONSTRAINT fk_grntcsnt_user FOREIGN KEY (user_id) REFERENCES public.user_entity(id);


--
-- Name: group_attribute fk_group_attribute_group; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.group_attribute
    ADD CONSTRAINT fk_group_attribute_group FOREIGN KEY (group_id) REFERENCES public.keycloak_group(id);


--
-- Name: group_role_mapping fk_group_role_group; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.group_role_mapping
    ADD CONSTRAINT fk_group_role_group FOREIGN KEY (group_id) REFERENCES public.keycloak_group(id);


--
-- Name: realm_enabled_event_types fk_h846o4h0w8epx5nwedrf5y69j; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_enabled_event_types
    ADD CONSTRAINT fk_h846o4h0w8epx5nwedrf5y69j FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: realm_events_listeners fk_h846o4h0w8epx5nxev9f5y69j; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_events_listeners
    ADD CONSTRAINT fk_h846o4h0w8epx5nxev9f5y69j FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: identity_provider_mapper fk_idpm_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.identity_provider_mapper
    ADD CONSTRAINT fk_idpm_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: idp_mapper_config fk_idpmconfig; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.idp_mapper_config
    ADD CONSTRAINT fk_idpmconfig FOREIGN KEY (idp_mapper_id) REFERENCES public.identity_provider_mapper(id);


--
-- Name: web_origins fk_lojpho213xcx4wnkog82ssrfy; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.web_origins
    ADD CONSTRAINT fk_lojpho213xcx4wnkog82ssrfy FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: org_invitation fk_org_invitation_org; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.org_invitation
    ADD CONSTRAINT fk_org_invitation_org FOREIGN KEY (organization_id) REFERENCES public.org(id) ON DELETE CASCADE;


--
-- Name: scope_mapping fk_ouse064plmlr732lxjcn1q5f1; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.scope_mapping
    ADD CONSTRAINT fk_ouse064plmlr732lxjcn1q5f1 FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: protocol_mapper fk_pcm_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.protocol_mapper
    ADD CONSTRAINT fk_pcm_realm FOREIGN KEY (client_id) REFERENCES public.client(id);


--
-- Name: credential fk_pfyr0glasqyl0dei3kl69r6v0; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.credential
    ADD CONSTRAINT fk_pfyr0glasqyl0dei3kl69r6v0 FOREIGN KEY (user_id) REFERENCES public.user_entity(id);


--
-- Name: protocol_mapper_config fk_pmconfig; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.protocol_mapper_config
    ADD CONSTRAINT fk_pmconfig FOREIGN KEY (protocol_mapper_id) REFERENCES public.protocol_mapper(id);


--
-- Name: default_client_scope fk_r_def_cli_scope_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.default_client_scope
    ADD CONSTRAINT fk_r_def_cli_scope_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: required_action_provider fk_req_act_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.required_action_provider
    ADD CONSTRAINT fk_req_act_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: resource_uris fk_resource_server_uris; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.resource_uris
    ADD CONSTRAINT fk_resource_server_uris FOREIGN KEY (resource_id) REFERENCES public.resource_server_resource(id);


--
-- Name: role_attribute fk_role_attribute_id; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.role_attribute
    ADD CONSTRAINT fk_role_attribute_id FOREIGN KEY (role_id) REFERENCES public.keycloak_role(id);


--
-- Name: realm_supported_locales fk_supported_locales_realm; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.realm_supported_locales
    ADD CONSTRAINT fk_supported_locales_realm FOREIGN KEY (realm_id) REFERENCES public.realm(id);


--
-- Name: user_federation_config fk_t13hpu1j94r2ebpekr39x5eu5; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_federation_config
    ADD CONSTRAINT fk_t13hpu1j94r2ebpekr39x5eu5 FOREIGN KEY (user_federation_provider_id) REFERENCES public.user_federation_provider(id);


--
-- Name: user_group_membership fk_user_group_user; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.user_group_membership
    ADD CONSTRAINT fk_user_group_user FOREIGN KEY (user_id) REFERENCES public.user_entity(id);


--
-- Name: policy_config fkdc34197cf864c4e43; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.policy_config
    ADD CONSTRAINT fkdc34197cf864c4e43 FOREIGN KEY (policy_id) REFERENCES public.resource_server_policy(id);


--
-- Name: identity_provider_config fkdc4897cf864c4e43; Type: FK CONSTRAINT; Schema: public; Owner: csfeer
--

ALTER TABLE ONLY public.identity_provider_config
    ADD CONSTRAINT fkdc4897cf864c4e43 FOREIGN KEY (identity_provider_id) REFERENCES public.identity_provider(internal_id);


--
-- PostgreSQL database dump complete
--

\unrestrict 01S3XTiIxztxGy9rZLcdd5kYk9Ybqh6QJzEnZOeBpEEo2P4PyYRRjWUVDqSAur4

