create extension postgis;

create table citation
(
    citation_id                    int generated by default as identity primary key,
    contact_lastname               varchar(255),
    contact_firstname              varchar(255),
    contact_email                  varchar(255),
    source_url                     varchar(255),
    pub_year                       int,
    pub_month                      int,
    pub_day                        int,
    citation_type                  varchar(255),
    tracer_select_statistical_test varchar(255),
    tracer_select_other            varchar(255),
    correction_organics            varchar(255),
    correction_grain_size          varchar(255),
    correction_other               varchar(255),
    apportionment_models           varchar(255),
    apportionment_statistical_test varchar(255),
    apportionment_other            varchar(255)
);

create table data_credit
(
    data_credit_id int generated by default as identity primary key,
    credit_type    varchar(255),
    credit_url     varchar(255),
    credit_contact varchar(255),
    access_year    int not null,
    access_month   int not null
);

create table sample_category
(
    category_id   int generated by default as identity primary key,
    category_name varchar(255) unique not null
);

create table sample
(
    sample_id            int generated by default as identity primary key,
    citation_id          int          not null,
    data_credit_id       int          not null,
    category_id          int          not null,
    location             geometry(point, 4326),
    location_description varchar(255),
    drainage_sqkm        double precision,
    sample_type          varchar(255) not null,
    grain_size_range_µm  varchar(255),
    grain_size_median_µm varchar(255),
    collection_year      int,
    collection_month     int,
    collection_tool      varchar(255),
    chronology_year      varchar(255),
    age_day              int,
    created_date         timestamptz default now(),
    updated_date         timestamptz default now(),

    constraint fk_sample_citation_id foreign key (citation_id) references citation (citation_id),
    constraint fk_sample_data_credit_id foreign key (data_credit_id) references data_credit (data_credit_id),
    constraint fk_sample_category_id foreign key (category_id) references sample_category (category_id)
);

create index fx_sample_category_id on sample (category_id);
create index fx_sample_citation_id on sample (citation_id);
create index fx_sample_data_credit_id on sample (data_credit_id);

create or replace function fn_after_update()
    returns trigger
    language  plpgsql
    as
$$
begin
    new.updated_date = now();
    return new;
end ;
$$;

create trigger tr_sample_date_updated
    after update of citation_id, data_credit_id, category_id, location, location_description, sample_type, grain_size_range_µm, grain_size_median_µm, collection_year, collection_month, collection_tool, chronology_year
    on sample
    for each row
    execute function fn_after_update();

create table tracer_fallout_radionuclide
(
    fallout_radionuclide_id int generated by default as identity primary key,
    sample_id               int unique not null,
    "210pb_pci_g"           double precision,
    "210pbex_pci_g"         double precision,
    "7be_mbq_g"             double precision,
    "10be_atoms_g"          double precision,
    "137cs_pci_g"           double precision,
    "226ra_pci_g"           double precision,

    constraint fk_traver_fallout_radionuclide_sample_id foreign key (sample_id) references sample (sample_id) on delete cascade
);

create index fx_tracer_fallout_radionuclide on tracer_fallout_radionuclide (sample_id);

create table tracer_inorganic
(
    inorganic_id int generated by default as identity primary key,
    sample_id    int,
    ag_mg_kg     numeric,
    al_mg_kg     numeric,
    as_mg_kg     numeric,
    au_ppb       numeric,
    b_mg_kg      numeric,
    ba_mg_kg     numeric,
    be_mg_kg     numeric,
    bi_mg_kg     numeric,
    br_mg_kg     numeric,
    ca_mg_kg     numeric,
    cd_mg_kg     numeric,
    ce_mg_kg     numeric,
    co_mg_kg     numeric,
    cr_mg_kg     numeric,
    cs_mg_kg     numeric,
    cu_mg_kg     numeric,
    dy_mg_kg     numeric,
    er_mg_kg     numeric,
    eu_mg_kg     numeric,
    fe_mg_kg     numeric,
    ga_mg_kg     numeric,
    gd_mg_kg     numeric,
    hf_mg_kg     numeric,
    hg_mg_kg     numeric,
    ho_mg_kg     numeric,
    k_mg_kg      numeric,
    la_mg_kg     numeric,
    li_mg_kg     numeric,
    lu_mg_kg     numeric,
    mg_mg_kg     numeric,
    mn_mg_kg     numeric,
    mo_mg_kg     numeric,
    na_mg_kg     numeric,
    nb_mg_kg     numeric,
    nd_mg_kg     numeric,
    ni_mg_kg     numeric,
    p_mg_kg      numeric,
    pb_mg_kg     numeric,
    pd_mg_kg     numeric,
    pr_mg_kg     numeric,
    pt_mg_kg     numeric,
    rb_mg_kg     numeric,
    s_mg_kg      numeric,
    sb_mg_kg     numeric,
    sc_mg_kg     numeric,
    se_mg_kg     numeric,
    si_mg_kg     numeric,
    sm_mg_kg     numeric,
    sn_mg_kg     numeric,
    sr_mg_kg     numeric,
    ta_mg_kg     numeric,
    tb_mg_kg     numeric,
    te_mg_kg     numeric,
    th_mg_kg     numeric,
    ti_mg_kg     numeric,
    tl_mg_kg     numeric,
    tm_mg_kg     numeric,
    u_mg_kg      numeric,
    v_mg_kg      numeric,
    w_mg_kg      numeric,
    y_mg_kg      numeric,
    yb_mg_kg     numeric,
    zn_mg_kg     numeric,
    zr_mg_kg     numeric,
    al2o3_ppm    numeric,
    cao_ppm      numeric,
    fe2o3_ppm    numeric,
    k2o_ppm      numeric,
    mgo_ppm      numeric,
    mno_ppm      numeric,
    na2o_ppm     numeric,
    p2o5_ppm     numeric,
    sio2_ppm     numeric,
    tio2_ppm     numeric,

    constraint fk_tracer_inorganic_sample_id foreign key (sample_id) references sample (sample_id) on delete cascade
);

create index fx_tracer_inorganic_sample_id on tracer_inorganic (sample_id);

create table tracer_isotope
(
    isotope_id    int generated by default as identity primary key,
    sample_id     int unique not null,
    "87sr_86sr"   numeric,
    "144nd_143nd" numeric,
    "206pb_204pb" numeric,
    "207pb_204pb" numeric,
    "208pb_204pb" numeric,
    d13c_permil   numeric,
    d15n_permil   numeric,

    constraint fk_tracer_isotope foreign key (sample_id) references sample (sample_id) on delete cascade
);

create index fx_tracer_isotope on tracer_isotope (sample_id);

create table tracer_organic
(
    organic_id        int generated by default as identity primary key,
    sample_id         int not null,
    poc_pc            numeric,
    toc_pc            numeric,
    ton_pc            numeric,
    lignin_mg_100mgoc numeric,

    constraint fk_tracer_organic_sample_id foreign key (sample_id) references sample (sample_id) on delete cascade
);

create index fx_tracer_organic on tracer_organic (sample_id);

create table tracer_other
(
    other_id  int generated by default as identity primary key,
    sample_id int not null,
    tc_pc     numeric,
    tn_pc     numeric,
    c_n_ratio numeric,

    constraint fk_tracer_other_sample_id foreign key (sample_id) references sample (sample_id) on delete cascade
);

create index fx_tracer_other_sample_id on tracer_other (sample_id);

