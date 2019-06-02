import Data.List.Split
import Data.List

-- ID, Имя, Темы +, Темы -, Преподаватели +, Преподаватели -, Текущий преподаватель
data Student = Student Integer String [Integer] [Integer] [Integer] [Integer] Integer deriving Show

-- ID, Имя, Темы +, Темы -, Студенты +, Студенты -, Текущие студенты
data Teacher = Teacher Integer String [Integer] [Integer] [Integer] [Integer] [Integer] deriving Show

getStudentId :: Student -> Integer
getStudentId (Student id name themesPositive themesNegative teachersPositive teachersNegative current) = id

parseIntegerLst :: String -> [Integer]
parseIntegerLst "" = [0]
parseIntegerLst lst = map (\(a) -> read a :: Integer) (splitOn ":" lst)

parseStudent :: [String] -> Student
parseStudent lst = Student 
    (read (lst!!0) :: Integer) 
    (lst!!1) 
    (parseIntegerLst $ lst!!2)
    (parseIntegerLst $ lst!!3)
    (parseIntegerLst $ lst!!4)
    (parseIntegerLst $ lst!!5)
    0

parseTeacher :: [String] -> Teacher
parseTeacher lst = Teacher
    (read (lst!!0) :: Integer) 
    (lst!!1) 
    (parseIntegerLst $ lst!!2)
    (parseIntegerLst $ lst!!3)
    (parseIntegerLst $ lst!!4)
    (parseIntegerLst $ lst!!5)
    []

splitData :: String -> [String]
splitData input = splitOn "\n" input

parseLine :: String -> [String]
parseLine line = splitOn ", " line

extractStudents :: [String] -> [Student]
extractStudents lines = map (\(line) -> parseStudent $ parseLine line) lines

extractTeachers :: [String] -> [Teacher]
extractTeachers lines = map (\(line) -> parseTeacher $ parseLine line) lines

intersectionRank :: [Integer] -> [Integer] -> Integer
intersectionRank left right = toInteger $ length $ (intersect) left right

estimateRelationValue :: Student -> Teacher -> Integer
estimateRelationValue 
    (Student s_id s_name s_themesPositive s_themesNegative s_teachersPositive s_teachersNegative s_current) 
    (Teacher t_id t_name t_themesPositive t_themesNegative t_studentsPositive t_studentsNegative t_current) = 
        (-10 * (intersectionRank s_themesPositive t_themesNegative)) +
        (-10 * (intersectionRank t_themesPositive s_themesNegative)) +
        (10 * (intersectionRank s_themesPositive t_themesPositive)) +
        (-100 * (
            (intersectionRank s_teachersNegative [t_id]) + (intersectionRank t_studentsNegative [s_id])
        )) +
        (100 * (
            (intersectionRank s_teachersPositive [t_id]) + (intersectionRank t_studentsPositive [s_id])
        ))

teacherMaxStudentsCap = 40

getTeacherCurrentStudents :: Teacher -> [Integer]
getTeacherCurrentStudents (Teacher t_id t_name t_themesPositive t_themesNegative t_studentsPositive t_studentsNegative t_current) =
    t_current

-- getMinCurrentLen :: [Teacher] -> Integer
-- getMinCurrentLen teachers = minimum (map (\(
--     Teacher _t_id _t_name _t_themesPositive _t_themesNegative _t_studentsPositive _t_studentsNegative _t_current
-- ) -> length _t_current) teachers

-- calculateRelations :: [Student] -> [Teacher] -> [String]
-- calculateRelations students teachers = map (\(
--     Student s_id s_name s_themesPositive s_themesNegative s_teachersPositive s_teachersNegative s_current
-- ) -> filter (\(teacher) -> 
--     (length (getTeacherCurrentStudents teacher) <= teacherMaxStudentsCap) && 
--     (length (getTeacherCurrentStudents teacher) == (getMinCurrentLen teachers)))
-- ) teachers)
--     students

main = do
    studentsData <- readFile "../data/students.csv"
    teachersData <- readFile "../data/teachers.csv"

    let studentsLines = splitData studentsData
    let teachersLines = splitData teachersData

    let students = extractStudents studentsLines
    let teachers = extractTeachers teachersLines

    let value = estimateRelationValue (students!!0) (teachers!!6) 
    putStrLn $ show value
    putStrLn $ show teacherMaxStudentsCap

    writeFile "output/students.csv" studentsData
    writeFile "output/teachers.csv" teachersData
