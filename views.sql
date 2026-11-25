-- Available Books View
CREATE OR REPLACE VIEW available_books AS
SELECT
    b.bookID,
    b.title,
    bc.copy_number,
    bc.availability_status
FROM books b, book_copy bc
WHERE b.bookID = bc.bookID
    AND bc.availability_status = 'Available';


-- Outstanding Fines View
CREATE OR REPLACE VIEW outstanding_fines AS
SELECT
    f.fineID,
    m.memberID,
    m.Fname,
    m.Lname,
    f.amount,
    f.paid_status,
    f.fine_due_date
FROM fine f, members_3nf m
WHERE f.memberID = m.memberID
    AND f.paid_status = 'Unpaid';


-- Borrowed Books View
CREATE OR REPLACE VIEW borrowed_books AS
SELECT
    b.bookID,
    b.title,
    br.borrow_date,
    br.due_date
FROM books b, borrows br
WHERE b.bookID = br.bookID
    AND br.return_date IS NULL;