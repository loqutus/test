drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  key text not null,
  value text not null
);