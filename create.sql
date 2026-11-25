-- Author Table
CREATE TABLE author (
    authorID NUMBER PRIMARY KEY,
    Fname VARCHAR2(25) NOT NULL,
    Lname VARCHAR2(25) NOT NULL,
    CONSTRAINT chk_author_id CHECK (authorID > 0)
);


-- Publisher Table
CREATE TABLE publisher (
    publisherID NUMBER PRIMARY KEY,
    name VARCHAR2(25) NOT NULL,
    address VARCHAR2(100),
    CONSTRAINT chk_publisher_id CHECK (publisherID > 0)
);


-- Books Table
CREATE TABLE books (
    bookID NUMBER PRIMARY KEY,
    ISBN VARCHAR2(25) NOT NULL UNIQUE,
    title VARCHAR2(25) NOT NULL,
    publication_year NUMBER NOT NULL,
    publisherID NUMBER NOT NULL REFERENCES publisher(publisherID),
    CONSTRAINT chk_book_id CHECK (bookID > 0),
    CONSTRAINT chk_publication_year CHECK (publication_year BETWEEN 1000 AND 2026)
);


-- Book Copy Table
CREATE TABLE book_copy (
    bookID NUMBER REFERENCES books(bookID),
    copy_number NUMBER,
    availability_status VARCHAR2(25) DEFAULT 'Available' NOT NULL,
    PRIMARY KEY (bookID, copy_number),
    CONSTRAINT chk_copy CHECK (bookID > 0 AND copy_number > 0),
    CONSTRAINT chk_availability CHECK (availability_status IN ('Available', 'Borrowed'))
);


-- Postal Location Table
CREATE TABLE postal_location (
    postal_code VARCHAR2(25) PRIMARY KEY,
    city VARCHAR2(25) NOT NULL,
    province VARCHAR2(25) NOT NULL
);


-- Normalized Members Table (3NF)
CREATE TABLE members_3nf (
    memberID NUMBER PRIMARY KEY,
    Fname VARCHAR2(25) NOT NULL,
    Lname VARCHAR2(25) NOT NULL,
    email VARCHAR2(25) NOT NULL UNIQUE,
    membership_date DATE DEFAULT SYSDATE NOT NULL,
    street VARCHAR2(25),
    postal_code VARCHAR2(25) REFERENCES postal_location(postal_code),
    CONSTRAINT chk_member_3nf_id CHECK (memberID > 0)
);


-- Librarian Table
CREATE TABLE librarian (
    librarianID NUMBER PRIMARY KEY,
    Fname VARCHAR2(25) NOT NULL,
    Lname VARCHAR2(25) NOT NULL,
    phone_num VARCHAR2(25),
    email VARCHAR2(25) NOT NULL UNIQUE,
    CONSTRAINT chk_librarian_id CHECK (librarianID > 0)
);


-- Fine Table
CREATE TABLE fine (
    fineID NUMBER PRIMARY KEY,
    amount NUMBER NOT NULL,
    paid_status VARCHAR2(25) DEFAULT 'Unpaid' NOT NULL,
    fine_date DATE DEFAULT SYSDATE NOT NULL,
    fine_due_date DATE NOT NULL,
    memberID NUMBER NOT NULL REFERENCES members_3nf(memberID),
    librarianID NUMBER NOT NULL REFERENCES librarian(librarianID),
    CONSTRAINT chk_fine CHECK (fineID > 0 AND amount >= 0),
    CONSTRAINT chk_paid_status CHECK (paid_status IN ('Paid', 'Unpaid')),
    CONSTRAINT chk_fine_dates CHECK (fine_due_date >= fine_date)
);


-- Writes Relationship Table
CREATE TABLE writes (
    authorID NUMBER REFERENCES author(authorID),
    bookID NUMBER REFERENCES books(bookID),
    PRIMARY KEY (authorID, bookID)
);


-- Borrows Relationship Table
CREATE TABLE borrows (
    memberID NUMBER REFERENCES members_3nf(memberID),
    bookID NUMBER REFERENCES books(bookID),
    borrow_date DATE,
    due_date DATE NOT NULL,
    return_date DATE,
    PRIMARY KEY (memberID, bookID, borrow_date),
    CONSTRAINT chk_borrow CHECK (memberID > 0 AND bookID > 0 AND borrow_date < due_date),
    CONSTRAINT chk_return CHECK (return_date IS NULL OR return_date >= borrow_date)
);


-- Reserves Relationship Table
CREATE TABLE reserves (
    memberID NUMBER REFERENCES members_3nf(memberID),
    bookID NUMBER REFERENCES books(bookID),
    reservation_date DATE,
    PRIMARY KEY (memberID, bookID, reservation_date)
);