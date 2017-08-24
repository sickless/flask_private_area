drop table if exists user;
create table user (
  iduser integer primary key autoincrement,
  username text not null,
  password text not null
);
