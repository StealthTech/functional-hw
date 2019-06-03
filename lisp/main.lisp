(defclass Student () 
    ((id
        :initarg :id
        :accessor id
    )(name
        :initarg :name
        :accessor name
    )(themesPositive
        :initarg :themesPositive
        :accessor themesPositive
    )(themesNegative
        :initarg :themesNegative
        :accessor themesNegative
    )(teachersPositive
        :initarg :teachersPositive
        :accessor teachersPositive
    )(teachersNegative 
        :initarg :teachersNegative
        :accessor teachersNegative
    )(currentTeacher 
        :initform nil
        :accessor currentTeacher
    ))
)

(defclass Teacher () 
    ((id
        :initarg :id
        :accessor id
    )(name
        :initarg :name
        :accessor name
    )(themesPositive
        :initarg :themesPositive
        :accessor themesPositive
    )(themesNegative
        :initarg :themesNegative
        :accessor themesNegative
    )(studentsPositive
        :initarg :studentsPositive
        :accessor studentsPositive
    )(studentsNegative 
        :initarg :studentsNegative
        :accessor studentsNegative
    )(currentStudents
        :initform nil
        :accessor currentStudents
    ))
)

(defclass Match () 
    ((mstudent
        :initarg :mstudent
        :accessor mstudent
    )(mteacher
        :initarg :mteacher
        :accessor mteacher
    )(mvalue
        :initarg :mvalue
        :accessor mvalue
    ))
)

(defvar teachersMaxStudentsCap 40)

(defun loadFile (filename)
    (with-open-file (stream filename)
        (loop for line = (read-line stream nil)
            while line
            collect line)))

(defun writeFile (filename content) (
    with-open-file (stream filename
        :direction :output
        :if-exists :overwrite
        :if-does-not-exist :create)
    (format stream content)
))

(defun _split (string &optional (separator " ") (r nil))
    (let ((n (position separator string
		    :from-end t
		    :test #'(lambda (x y)
			        (find y x :test #'string=)))))
    (if n (_split (subseq string 0 n) separator (cons (subseq string (1+ n)) r)) (cons string r))
))

(defun split (string &optional (separator " ")) (
    _split string separator
))

(defun splitLines (lines) (
    mapcar #'(lambda(x) (split x ",")) lines
))

(defun splitStrIntList (str) (
    if (= (length str) 0) nil (mapcar #'(lambda (x) (parse-integer x)) (split str ":"))
))

(defun trim (str) (
    string-trim '(#\Space #\Newline #\Backspace #\Tab #\Linefeed #\Page #\Return #\Rubout) str
))

(defun parseStudent (line) (
    make-instance 'Student 
        :id (parse-integer (trim (nth 0 line)))
        :name (trim (nth 1 line))
        :themesPositive (splitStrIntList (trim (nth 2 line)))
        :themesNegative (splitStrIntList (trim (nth 3 line)))
        :teachersPositive  (splitStrIntList (trim (nth 4 line)))
        :teachersNegative (splitStrIntList (trim (nth 5 line)))
))

(defun parseTeacher (line) (
    make-instance 'Teacher
        :id (parse-integer (trim (nth 0 line)))
        :name (trim (nth 1 line))
        :themesPositive (splitStrIntList (trim (nth 2 line)))
        :themesNegative (splitStrIntList (trim (nth 3 line)))
        :studentsPositive  (splitStrIntList (trim (nth 4 line)))
        :studentsNegative (splitStrIntList (trim (nth 5 line)))
))

(defun extractStudents (lst) 
    (mapcar #'(lambda(x) (parseStudent x)) lst
))

(defun extractTeachers (lst) 
    (mapcar #'(lambda(x) (parseTeacher x)) lst
))

(defun intersectionRank (left right) (
    list-length (intersection left right)
))

(defun estimateRelationValue (student teacher) (
        +
        (* -10 (intersectionRank (themesPositive student) (themesNegative teacher)))
        (* -10 (intersectionRank (themesPositive teacher) (themesNegative student)))
        (* 10 (intersectionRank (themesPositive student) (themesPositive teacher)))
        (* -100 (
            +
            (intersectionRank (teachersNegative student) (list (id teacher))) 
            (intersectionRank (studentsNegative teacher) (list (id student)))
        ))
        (* 100 (
            +
            (intersectionRank (teachersPositive student) (list (id teacher)))
            (intersectionRank (studentsPositive teacher) (list (id student)))
        ))
    ))

(defun smallest (lst)
    (apply 'min lst)
)

(defun filter (condp lst) (
    mapcar (lambda (x) (and (funcall condp x) x)) lst
))

(defun joinComma (lst) 
    (format nil "~{~A~^, ~}" lst))


(defun joinCaret (lst) 
    (format nil "~{~A~^~%~}" lst))

(defun getMinCurrentLen (teachers) (
    smallest (
        mapcar #'(
            lambda (teacher) (list-length (currentStudents teacher))
        ) teachers
    )
))

(defun validateTeacher (teacher teachers) (
    and
    (<= (list-length (currentStudents teacher)) 40)
    (= (list-length (currentStudents teacher)) (getMinCurrentLen teachers))
))

(defun comparatorSnd (a b) (
    > (nth 1 a) (nth 1 b)
))

(defun getMatch (student teacher value) 
    (make-instance 'Match
        :mstudent student
        :mteacher teacher
        :mvalue value
))

(defun partialCalcRelations (student teachers) (
    loop for teacher in teachers
        do (
            let ((_teachers (filter #'(lambda (teacher) (validateTeacher teacher teachers)) teachers ))) (
                let ((_values (
                    mapcar #'(lambda (_teacher) (list _teacher (estimateRelationValue student _teacher))) _teachers
                ))) (
                    let ((_pack (nth 0 (sort _values 'comparatorSnd)))) (
                        let ((_teacher (nth 0 _pack)) (value (nth 1 _pack))) (
                            return (getMatch student _teacher value)
                        )
                    )
                )
            )
        )
))

(defun makeLineFromMatch (match) (
    joinComma (list (id (mstudent match)) (id (mteacher match)) (mvalue match))
))

(defun calculateRelations (students teachers) (
    mapcar #'(lambda (student) (partialCalcRelations student teachers)) students
))

(defvar studentsLines (loadFile "../data/students.csv"))
(defvar teachersLines (loadFile "../data/teachers.csv"))

(defvar students (extractStudents(splitLines studentsLines)))
(defvar teachers (extractTeachers(splitLines teachersLines)))

(defvar relations (mapcar #'(lambda (match) (makeLineFromMatch match)) (calculateRelations students teachers)))

(defvar output (joinCaret relations))

(writeFile "output/relations.csv" output)
