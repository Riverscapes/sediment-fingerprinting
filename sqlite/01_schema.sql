create table tracer_types
(
    tracer_type_id   integer not null primary key autoincrement,
    tracer_type_name text    not null unique
);

create table analytical_methods
(
    analytical_method_id   integer not null primary key autoincrement,
    analytical_method_name text    not null,
    tracer_group           text,
    method_description     text,
    method_url             text
);
create unique index ux_analytical_methods_analytical_method_name on analytical_methods (analytical_method_name);

create table citations
(
    citation_id                    integer not null primary key autoincrement,
    contact_last_name              text,
    contact_first_name             text,
    contact_email                  text,
    source_url                     text,
    pub_year                       integer,
    pub_month                      integer,
    pub_day                        integer,
    type                           text,
    tracer_select_statistical_test text,
    tracer_select_other            text,
    correction_organics            text,
    correction_grain_size          text,
    correction_other               text,
    apportionment_models           text,
    apportionment_statistical_test text,
    apportionment_other            text
);


create table data_credits
(
    data_credit_id integer not null primary key autoincrement,
    credit_type    text,
    credit_url     text,
    credit_contact text,
    access_year    integer not null,
    access_month   integer not null
);

create table sample_categories
(
    category_id   integer not null primary key autoincrement,
    category_type text    not null unique
);


create table samples
(
    sample_id                 integer not null primary key autoincrement,
    citation_id               integer not null references citations (citation_id),
    data_credit_id            integer not null references data_credits (data_credit_id),
    category_id               integer not null references sample_categories (category_id),
    location_latitude         real,
    location_longitude        real,
    location_description      text,
    drainage_sq_km            real,
    sample_type               text    not null,
    grain_size_range_micro_m  text,
    grain_size_median_micro_m text,
    collection_year           integer,
    collection_month          integer,
    collection_tool           text,
    chronology_year           text,
    sampling_period_day       integer,
    created_date              date default current_timestamp not null,
    updated_date              date default current_timestamp not null
);

create index fx_sample_category_id on samples (category_id);
create index fx_sample_citation_id on samples (citation_id);
create index fx_sample_data_credit_id on samples (data_credit_id);

create table sample_analytical_methods
(
    sample_id            integer not null references samples (sample_id) on delete cascade,
    tracer_type_id       integer not null references tracer_types (tracer_type_id),
    analytical_method_id integer not null references analytical_methods (analytical_method_id),

    constraint pk_sample_analytical_methods primary key (sample_id, tracer_type_id, analytical_method_id)
);
create index fx_tracer_type_id on sample_analytical_methods (tracer_type_id);
create index fx_analytical_method_id on sample_analytical_methods (analytical_method_id);

create table tracer_organic
(
    sample_id         integer not null primary key references samples (sample_id) on delete cascade,
    poc_pc            real,
    toc_pc            real,
    ton_pc            real,
    lignin_mg_100mgoc real
);


create table tracer_inorganic
(
    sample_id integer not null primary key references samples (sample_id) on delete cascade,
    ag_mg_kg  real,
    al_mg_kg  real,
    as_mg_kg  real,
    au_ppb    real,
    b_mg_kg   real,
    ba_mg_kg  real,
    be_mg_kg  real,
    bi_mg_kg  real,
    br_mg_kg  real,
    ca_mg_kg  real,
    cd_mg_kg  real,
    ce_mg_kg  real,
    co_mg_kg  real,
    cr_mg_kg  real,
    cs_mg_kg  real,
    cu_mg_kg  real,
    dy_mg_kg  real,
    er_mg_kg  real,
    eu_mg_kg  real,
    fe_mg_kg  real,
    ga_mg_kg  real,
    gd_mg_kg  real,
    ge_mg_kg  real,
    hf_mg_kg  real,
    hg_mg_kg  real,
    ho_mg_kg  real,
    in_mg_kg  real,
    k_mg_kg   real,
    la_mg_kg  real,
    li_mg_kg  real,
    lu_mg_kg  real,
    mg_mg_kg  real,
    mn_mg_kg  real,
    mo_mg_kg  real,
    na_mg_kg  real,
    nb_mg_kg  real,
    nd_mg_kg  real,
    ni_mg_kg  real,
    p_mg_kg   real,
    pb_mg_kg  real,
    pd_mg_kg  real,
    pr_mg_kg  real,
    pt_mg_kg  real,
    rb_mg_kg  real,
    re_mg_kg  real,
    s_mg_kg   real,
    sb_mg_kg  real,
    sc_mg_kg  real,
    se_mg_kg  real,
    si_mg_kg  real,
    sm_mg_kg  real,
    sn_mg_kg  real,
    sr_mg_kg  real,
    ta_mg_kg  real,
    tb_mg_kg  real,
    te_mg_kg  real,
    th_mg_kg  real,
    ti_mg_kg  real,
    tl_mg_kg  real,
    tm_mg_kg  real,
    u_mg_kg   real,
    v_mg_kg   real,
    w_mg_kg   real,
    y_mg_kg   real,
    yb_mg_kg  real,
    zn_mg_kg  real,
    zr_mg_kg  real,
    al2o3_ppm real,
    cao_ppm   real,
    fe2o3_ppm real,
    k2o_ppm   real,
    mgo_ppm   real,
    mno_ppm   real,
    na2o_ppm  real,
    p2o5_ppm  real,
    sio2_ppm  real,
    tio2_ppm  real
);

create table tracer_fallout_radionuclide
(
    sample_id         integer not null primary key references samples (sample_id) on delete cascade,
    "210pb_pci_g"     real,
    "210pbex_pci_g"   real,
    "7be_mbq_g"       real,
    "10be_atoms_g"    real,
    "137cs_pci_g"     real,
    "226ra_pci_g"     real,
    "238u_pci_g"      real,
    "238pu_pci_g"     real,
    "239_240pu_pci_g" real,
    "212bi_pci_g"     real,
    "214bi_pci_g"     real,
    "212pb_pci_g"     real,
    "214pb_pci_g"     real,
    "228ac_pci_g"     real,
    "40k_pci_g"       real,
    "208tl_pci_g"     real,
    "60co_pci_g"      real,
    "89sr_pci_g"      real,
    "234th_pci_g"     real,
    "235u_pci_g"      real
);

create table tracer_isotope
(
    sample_id     integer not null primary key references samples (sample_id) on delete cascade,
    "87sr_86sr"   real,
    "144nd_143nd" real,
    "206pb_204pb" real,
    "206pb_207pb" real,
    "206pb_208pb" real,
    "207pb_204pb" real,
    "208pb_204pb" real,
    d13c_permil   real,
    d15n_permil   real
);

create index fx_tracer_isotope
    on tracer_isotope (sample_id);



create table tracer_other
(
    sample_id       integer not null primary key references samples (sample_id) on delete cascade,
    tc_pc           real,
    tn_pc           real,
    c_n_molar_ratio real
);

create view vw_analytical_methods as
    SELECT sam.sample_id,
       tt.tracer_type_name,
       am.analytical_method_name
  FROM sample_analytical_methods sam
       INNER JOIN
       tracer_types tt ON sam.tracer_type_id
       INNER JOIN
       analytical_methods am ON sam.analytical_method_id = am.analytical_method_id;
