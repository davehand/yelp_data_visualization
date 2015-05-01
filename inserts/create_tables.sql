Create table business (
  business_id char(22) not null,
  name varchar2(100),
  full_address varchar2(150),
  city varchar2(50),
  state varchar2(5),
  latitude varchar2(20),
  longitude varchar2(20),
  CONSTRAINT business_id_pk PRIMARY KEY (business_id)
);

Create table business_category (
  business_id char(22) not null,
  category varchar2(50) not null,
  CONSTRAINT business_category_pk PRIMARY KEY (business_id, category),
  CONSTRAINT fk_business_id
    FOREIGN KEY (business_id)
    REFERENCES business(business_id)
);

Create table review (
  review_id char(22) not null,
  business_id char(22) not null,
  stars number(1),
  useful_votes number(10),
  review_date date,
  CONSTRAINT business_review_pk PRIMARY KEY (review_id, business_id),
  CONSTRAINT fk_business_id2
    FOREIGN KEY (business_id)
    REFERENCES business(business_id)
);

Create table searches (
  facebook_login varchar2(50) not null,
  search_text varchar2(100) not null,
  CONSTRAINT login_search_pk PRIMARY KEY (facebook_login, search_text)
);

