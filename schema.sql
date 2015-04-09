drop table if exists entries;

create table entries (
	id integer primary key autoincrement,
	url string not null UNIQUE,
        image_url string not null,
        excerpt string not null,
        source string not null,
        updated timestamp not null,
        last_refresh timestamp not null);
        	 
drop table if exists papers;

create table papers (
	id integer primary key autoincrement,
    title string not null,
    updated timestamp not null,
    content BLOB);
