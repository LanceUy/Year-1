from course import Student, Course
import course
import criterion
from criterion import HomogeneousCriterion, LonelyMemberCriterion, \
    HeterogeneousCriterion, InvalidAnswerError
import grouper
import survey
from typing import List, Set, FrozenSet
import pytest


@pytest.fixture
def empty_course() -> course.Course:
    return course.Course('csc148')


@pytest.fixture
def students() -> List[course.Student]:
    return [course.Student(1, 'Zoro'),
            course.Student(2, 'Aaron'),
            course.Student(3, 'Gertrude'),
            course.Student(4, 'Yvette')]


@pytest.fixture
def alpha_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def greedy_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[1],
                                      students_with_answers[3]]))
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[2]]))
    return grouping


@pytest.fixture
def window_grouping(students_with_answers) -> grouper.Grouping:
    grouping = grouper.Grouping()
    grouping.add_group(grouper.Group([students_with_answers[0],
                                      students_with_answers[1]]))
    grouping.add_group(grouper.Group([students_with_answers[2],
                                      students_with_answers[3]]))
    return grouping


@pytest.fixture
def questions() -> List[survey.Question]:
    return [survey.MultipleChoiceQuestion(1, 'why?', ['a', 'b']),
            survey.NumericQuestion(2, 'what?', -2, 4),
            survey.YesNoQuestion(3, 'really?'),
            survey.CheckboxQuestion(4, 'how?', ['a', 'b', 'c'])]


@pytest.fixture
def criteria(answers) -> List[criterion.Criterion]:
    return [criterion.HomogeneousCriterion(),
            criterion.HeterogeneousCriterion(),
            criterion.LonelyMemberCriterion()]


@pytest.fixture()
def weights() -> List[int]:
    return [2, 5, 7]


@pytest.fixture
def answers() -> List[List[survey.Answer]]:
    return [[survey.Answer('a'), survey.Answer('b'),
             survey.Answer('a'), survey.Answer('b')],
            [survey.Answer(0), survey.Answer(4),
             survey.Answer(-1), survey.Answer(1)],
            [survey.Answer(True), survey.Answer(False),
             survey.Answer(True), survey.Answer(True)],
            [survey.Answer(['a', 'b']), survey.Answer(['a', 'b']),
             survey.Answer(['a']), survey.Answer(['b'])]]


@pytest.fixture
def students_with_answers(students, questions, answers) -> List[course.Student]:
    for i, student in enumerate(students):
        for j, question in enumerate(questions):
            student.set_answer(question, answers[j][i])
    return students


@pytest.fixture
def course_with_students(empty_course, students) -> course.Course:
    empty_course.enroll_students(students)
    return empty_course


@pytest.fixture
def course_with_students_with_answers(empty_course,
                                      students_with_answers) -> course.Course:
    empty_course.enroll_students(students_with_answers)
    return empty_course


@pytest.fixture
def survey_(questions, criteria, weights) -> survey.Survey:
    s = survey.Survey(questions)
    for i, question in enumerate(questions):
        if i:
            s.set_weight(weights[i - 1], question)
        if len(questions) - 1 != i:
            s.set_criterion(criteria[i], question)
    return s


@pytest.fixture
def group(students) -> grouper.Group:
    return grouper.Group(students)


def get_member_ids(grouping: grouper.Grouping) -> Set[FrozenSet[int]]:
    member_ids = set()
    for group in grouping.get_groups():
        ids = []
        for member in group.get_members():
            ids.append(member.id)
        member_ids.add(frozenset(ids))
    return member_ids


def compare_groupings(grouping1: grouper.Grouping,
                      grouping2: grouper.Grouping) -> None:
    assert get_member_ids(grouping1) == get_member_ids(grouping2)


def test_student_name() -> None:
    """Simple test case for str(Student)"""
    student = Student(1, 'Jack')
    assert str(student) == 'Jack'


def test_student_has_answer_for_basic_yes_no_question() -> None:
    """Check for simplest case of Student.has_answer(Question).
    Student either has answer, or does not."""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    question = survey.YesNoQuestion(1, 'Are you over 18?')
    question2 = survey.YesNoQuestion(2, 'Are you in first year?')
    answer = survey.Answer(True)
    student1.set_answer(question, answer)
    student2.set_answer(question2, answer)
    assert student1.has_answer(question)
    assert student2.has_answer(question2)
    assert not student2.has_answer(question)
    assert not student1.has_answer(question2)


def test_student_has_answer_for_basic_multiple_choice() -> None:
    """Check """
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    student6 = Student(6, 'Markus')
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    answer1 = survey.Answer('1st')
    answer2 = survey.Answer('2nd')
    answer3 = survey.Answer('3rd')
    answer4 = survey.Answer('4th')
    answer5 = survey.Answer('past 4th')
    student1.set_answer(question, answer1)
    student2.set_answer(question, answer2)
    student3.set_answer(question, answer3)
    student4.set_answer(question, answer4)
    student5.set_answer(question, answer5)
    assert student1.has_answer(question)
    assert student2.has_answer(question)
    assert student3.has_answer(question)
    assert student4.has_answer(question)
    assert student5.has_answer(question)
    assert not student6.has_answer(question)


def test_student_has_answer_for_basic_numeric_question() -> None:
    """Check for whether a student has an answer,
    or not for a NumbericQuestion"""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    question = survey.NumericQuestion(1,
                                      'How much do you know about this topic?',
                                      1, 5)
    answer = survey.Answer(4)
    student1.set_answer(question, answer)
    assert student1.has_answer(question)
    assert not student2.has_answer(question)


def test_student_has_answer_for_basic_checkbox_question() -> None:
    """Check for whether a student has an answer or not
    for a CheckboxQuestion."""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    question = survey.CheckboxQuestion(1, 'Which courses have you taken?',
                                       ['CSC104', 'CSC108', 'CSC165'])
    answer = survey.Answer(['CSC108', 'CSC165'])
    student1.set_answer(question, answer)
    assert student1.has_answer(question)
    assert not student2.has_answer(question)


def test_student_set_answer_all_types() -> None:
    """Check Student.set_answer(Question, Answer) for all types of questions
    and their respective valid answers"""
    student1 = Student(1, 'Jack')
    student2 = Student(1, 'Mike')
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    question2 = survey.YesNoQuestion(2, 'Are you in first year?')
    question3 = survey.NumericQuestion(1,
                                       'How much do you know about this topic?',
                                       1, 5)
    question4 = survey.CheckboxQuestion(1, 'Which courses have you taken?',
                                        ['CSC104', 'CSC108', 'CSC165'])
    answer = survey.Answer(True)
    answer2 = survey.Answer(False)
    answer3 = survey.Answer('1st')
    answer4 = survey.Answer(3)
    answer5 = survey.Answer('CSC104')
    student1.set_answer(question2, answer)
    student2.set_answer(question2, answer2)
    student1.set_answer(question, answer3)
    student1.set_answer(question3, answer4)
    student1.set_answer(question4, answer5)
    assert student1.get_answer(question).content == '1st'
    assert student1.get_answer(question2).content
    assert student1.get_answer(question3).content == 3
    assert student1.get_answer(question4).content == 'CSC104'
    assert not student2.get_answer(question2).content


def test_student_get_answer_no_answer() -> None:
    student1 = Student(1, 'Jack')
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    assert student1.get_answer(question) is None


def test_course_enroll_students_same_id() -> None:
    """Check Course.enroll_students on a list of students with repeating ids"""
    student1 = Student(1, 'Jack')
    student2 = Student(1, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    lst = [student1, student2, student3, student4]
    course_ = Course('CSC148')
    course_.enroll_students(lst)
    assert course_.students == []


def test_course_enroll_students_4_students() -> None:
    """Check Course.enroll_students on a list of 4 students"""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    lst = [student1, student2, student3, student4]
    course_ = Course('CSC148')
    course_.enroll_students(lst)
    assert course_.students == lst


def test_course_enroll_students_empty_list() -> None:
    """Check Course.enroll_students on an empty list"""
    course_ = Course('CSC148')
    course_.enroll_students([])
    assert course_.students == []


def test_course_all_answered_empty_course() -> None:
    """Test Course.enroll_students on a course with no students

    This should be vacuously True
    """
    course_ = Course('CSC148')
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    survey_ = survey.Survey([question])
    assert course_.all_answered(survey_)


def test_course_all_answered_one_question_one_student_no_answer() -> None:
    """Test Course.enroll_students on a course with 1 student
    and a survey with 1 question but student has no answer"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    survey_ = survey.Survey([question])
    course_.enroll_students([student1])
    assert not course_.all_answered(survey_)


def test_course_all_answered_one_question_one_student_invalid_answer() -> None:
    """Test Course.enroll_students on a course with 1 student
    and a survey with 1 question but student has no valid answer"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    answer = survey.Answer('Yes')
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    student1.set_answer(question, answer)
    survey_ = survey.Survey([question])
    course_.enroll_students([student1])
    assert not course_.all_answered(survey_)


def test_course_all_answered_one_question_one_student_valid_answer() -> None:
    """Test Course.enroll_students on a course with 1 student
    and a survey with 1 question and student has valid answer"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    answer = survey.Answer(True)
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    student1.set_answer(question, answer)
    survey_ = survey.Survey([question])
    course_.enroll_students([student1])
    assert course_.all_answered(survey_)


def test_course_all_answered_one_question_multiple_student_valid_answer() -> \
        None:
    """Test Course.enroll_students on a course with 2 student
    and a survey with 1 question and both students has valid answers"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    answer = survey.Answer(True)
    answer2 = survey.Answer(False)
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    student1.set_answer(question, answer)
    student2.set_answer(question, answer2)
    survey_ = survey.Survey([question])
    course_.enroll_students([student1, student2])
    assert course_.all_answered(survey_)


def test_course_all_answered_one_question_multiple_student_invalid_answer() -> \
        None:
    """Test Course.enroll_students on a course with 2 student
    and a survey with 1 question and one students has an invalid answer"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    answer = survey.Answer(True)
    answer2 = survey.Answer('No')
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    student1.set_answer(question, answer)
    student2.set_answer(question, answer2)
    survey_ = survey.Survey([question])
    course_.enroll_students([student1, student2])
    assert not course_.all_answered(survey_)


def test_course_all_answered_multiple_question_and_students_valid_answer() \
        -> None:
    """Test Course.enroll_students on a course with 2 student
    and a survey with 2 question and all students has valid answers"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    answer = survey.Answer(True)
    answer2 = survey.Answer(False)
    answer3 = survey.Answer(3)
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    question2 = survey.NumericQuestion(1,
                                       'How much do you know about this topic?',
                                       1, 5)
    student1.set_answer(question, answer)
    student2.set_answer(question, answer2)
    student1.set_answer(question2, answer3)
    student2.set_answer(question2, answer3)
    survey_ = survey.Survey([question, question2])
    course_.enroll_students([student1, student2])
    assert course_.all_answered(survey_)


def test_course_all_answered_multiple_question_and_students_invalid_answer() \
        -> None:
    """Test Course.enroll_students on a course with 2 student
    and a survey with 2 question and one student has an invalid answer"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    answer = survey.Answer(True)
    answer2 = survey.Answer('No')
    answer3 = survey.Answer(3)
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    question2 = survey.NumericQuestion(1,
                                       'How much do you know about this topic?',
                                       1, 5)
    student1.set_answer(question, answer)
    student2.set_answer(question, answer2)
    student1.set_answer(question2, answer3)
    student2.set_answer(question2, answer3)
    survey_ = survey.Survey([question, question2])
    course_.enroll_students([student1, student2])
    assert not course_.all_answered(survey_)


def test_course_all_answered_no_questions_and_students_valid_answers() \
        -> None:
    """Test Course.enroll_students on a course with 2 student
    and a survey with 2 question and one student has an invalid answer

    This should be vacuously True.
    """
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    answer = survey.Answer(True)
    answer2 = survey.Answer(False)
    answer3 = survey.Answer(3)
    question = survey.YesNoQuestion(2, 'Are you in first year?')
    question2 = survey.NumericQuestion(1,
                                       'How much do you know about this topic?',
                                       1, 5)
    student1.set_answer(question, answer)
    student2.set_answer(question, answer2)
    student1.set_answer(question2, answer3)
    student2.set_answer(question2, answer3)
    survey_ = survey.Survey([])
    course_.enroll_students([student1, student2])
    assert course_.all_answered(survey_)


def test_course_get_students_no_students() -> None:
    """Tests Course.get_students with a course of no students"""
    course_ = Course('CSC148')
    course_.enroll_students([])
    assert course_.get_students() == ()


def test_course_get_students_one_student() -> None:
    """Tests Course.get_students with a course of one student"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    course_.enroll_students([student1])
    assert course_.get_students() == (student1,)


def test_course_get_students_multiple_students() -> None:
    """Tests Course.get_students with a course of two students"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    course_.enroll_students([student1, student2])
    assert course_.get_students() == (student1, student2)


def test_course_get_students_multiple_students_reverse_order_ids() -> None:
    """Tests Course.get_students with a course of two students but the
    students are enrolled in the course with ids in reverse order"""
    course_ = Course('CSC148')
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    course_.enroll_students([student2, student1])
    assert course_.get_students() == (student1, student2)


def test_multiplechoicequestion_str_no_answers() -> None:
    """Test str(MultipleChoiceQuestion) with no answers"""
    mc = survey.MultipleChoiceQuestion(1, 'Empty question?', [])
    assert str(mc) == 'Empty question?: []'


def test_multiplechoicequestion_str_answers() -> None:
    """Test str(MultipleChoiceQuestion) with answers"""
    mc = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                       ['1st', '2', '3rd', '4th'])
    assert str(mc) == 'Which year are you in?: [\'1st\', ' \
                      '\'2\', \'3rd\', \'4th\']'


def test_multiplechoicequestion_validate_answer_valid_answer() -> None:
    """Test MultipleChoiceQuestion.validate_answer with valid answers"""
    mc = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                       ['1st', '2', '3rd', '4th'])
    answer = survey.Answer('1st')
    assert mc.validate_answer(answer)


def test_slice_list_odd_length_odd_slice_length() -> None:
    """Test test_slice on an odd list with each slice having an odd length"""
    lst = [1, 2, 3, 4, 5]
    n = 3
    assert grouper.slice_list(lst, n) == [[1, 2, 3], [4, 5]]


def test_slice_list_odd_length_even_slice_length() -> None:
    """Test test_slice on an odd list with each slice having an even length"""
    lst = [1, 2, 3, 4, 5]
    n = 2
    assert grouper.slice_list(lst, n) == [[1, 2], [3, 4], [5]]


def test_slice_list_even_length_even_slice_length() -> None:
    """Test test_slice on an even list with each slice having an even length"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 2
    assert grouper.slice_list(lst, n) == [[1, 2], [3, 4], [5, 6]]


def test_slice_list_even_length_odd_slice_length() -> None:
    """Test test_slice on an even list with each slice having an odd length"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 3
    assert grouper.slice_list(lst, n) == [[1, 2, 3], [4, 5, 6]]


def test_slice_list_zero_length_slices() -> None:
    """Test test_slice on an even list with each slice having an
        odd length"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 0
    assert grouper.slice_list(lst, n) == []


def test_slice_list_empty_list() -> None:
    """Test test_slice on an empty list"""
    lst = []
    n = 0
    assert grouper.slice_list(lst, n) == []


def test_slice_list_slice_length_1() -> None:
    """Test test_slice on an even list with each slice having an odd length"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 1
    assert grouper.slice_list(lst, n) == [[1], [2], [3], [4], [5], [6]]


def test_slice_list_length_equals_slice_length() -> None:
    """Test test_slice on a list with each slice having the same length as
    the list"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 6
    assert grouper.slice_list(lst, n) == [lst]


def test_slice_list_list_of_iterables() -> None:
    """Test slice_list on a list or iterable objects"""
    lst = [[1, 2], [3, 4], [5, 6]]
    n = 2
    assert grouper.slice_list(lst, n) == [[[1, 2], [3, 4]], [[5, 6]]]


def test_windows_odd_length_odd_slice_length() -> None:
    """Test windows on an odd list with each slice having an odd length"""
    lst = [1, 2, 3, 4, 5]
    n = 3
    assert grouper.windows(lst, n) == [[1, 2, 3], [2, 3, 4], [3, 4, 5]]


def test_windows_odd_length_even_slice_length() -> None:
    """Test windows on an odd list with each slice having an even length"""
    lst = [1, 2, 3, 4, 5]
    n = 2
    assert grouper.windows(lst, n) == [[1, 2], [2, 3], [3, 4], [4, 5]]


def test_windows_even_length_even_slice_length() -> None:
    """Test windows on an even list with each slice having an even length"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 2
    assert grouper.windows(lst, n) == [[1, 2], [2, 3], [3, 4],
                                       [4, 5], [5, 6]]


def test_windows_even_length_odd_slice_length() -> None:
    """Test windows on an even list with each slice having an odd length"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 3
    assert grouper.windows(lst, n) == [[1, 2, 3], [2, 3, 4],
                                       [3, 4, 5], [4, 5, 6]]


def test_windows_zero_length_slices() -> None:
    """Test windows on an even list with each slice having an
        odd length"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 0
    assert grouper.windows(lst, n) == []


def test_windows_empty_list() -> None:
    """Test windows on an empty list"""
    lst = []
    n = 0
    assert grouper.windows(lst, n) == []


def test_windows_slice_length_1() -> None:
    """Test windows on an even list with each slice having an odd length"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 1
    assert grouper.windows(lst, n) == [[1], [2], [3], [4], [5], [6]]


def test_windows_length_equals_slice_length() -> None:
    """Test windows on a list with each slice having the same length as
    the list"""
    lst = [1, 2, 3, 4, 5, 6]
    n = 6
    assert grouper.windows(lst, n) == [lst]


def test_windows_list_of_iterables() -> None:
    """Test windows on a list or iterable objects"""
    lst = [[1, 2], [3, 4], [5, 6]]
    n = 2
    assert grouper.windows(lst, n) == [[[1, 2], [3, 4]], [[3, 4], [5, 6]]]


def test_alphagrouper_one_question_two_students() -> None:
    """Test AlphaGrouper.make_group with a survey of 1 questions and a
    class of 2 students"""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    students = [student1, student2]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    answer1 = survey.Answer('1st')
    answer2 = survey.Answer('2nd')
    student1.set_answer(question, answer1)
    student2.set_answer(question, answer2)
    questions = [question]
    survey_ = survey.Survey(questions)
    alpha = grouper.AlphaGrouper(2)
    theoretical_grouping = grouper.Grouping()
    theoretical_grouping.add_group(grouper.Group(students))
    compare_groupings(alpha.make_grouping(course_, survey_),
                      theoretical_grouping)


def test_alphagrouper_no_question_two_students() -> None:
    """Test AlphaGrouper.make_group with a survey of no question and a
    class of 2 students"""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    students = [student1, student2]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    questions = []
    survey_ = survey.Survey(questions)
    alpha = grouper.AlphaGrouper(2)
    theoretical_grouping = grouper.Grouping()
    theoretical_grouping.add_group(grouper.Group(students))
    compare_groupings(alpha.make_grouping(course_, survey_),
                      theoretical_grouping)


def test_alphagrouper_no_question_two_students_inverted_order() -> None:
    """Test AlphaGrouper.make_group with a survey of no question and a
    class of 2 students who are enrolled in the class not in alphabetical
     order"""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    students = [student2, student1]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    questions = []
    survey_ = survey.Survey(questions)
    alpha = grouper.AlphaGrouper(2)
    theoretical_grouping = grouper.Grouping()
    theoretical_grouping.add_group(grouper.Group(students))
    compare_groupings(alpha.make_grouping(course_, survey_),
                      theoretical_grouping)


def test_alphagrouper_multiple_questions_3_students() -> None:
    """Test AlphaGrouper.make_group with a survey of 2 question and a
    class of 3 students"""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Natalie')
    students = [student1, student2, student3]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    question2 = survey.YesNoQuestion(2, 'Are you over 18?')
    answer1 = survey.Answer('1st')
    answer2 = survey.Answer('2nd')
    answert = survey.Answer(True)
    answerf = survey.Answer(False)
    student1.set_answer(question, answer1)
    student2.set_answer(question, answer2)
    student3.set_answer(question2, answer1)
    student1.set_answer(question2, answert)
    student2.set_answer(question2, answerf)
    student3.set_answer(question2, answerf)
    questions = [question, question2]
    survey_ = survey.Survey(questions)
    alpha = grouper.AlphaGrouper(2)
    theoretical_grouping = grouper.Grouping()
    theoretical_grouping.add_group(grouper.Group(students[:2]))
    theoretical_grouping.add_group(grouper.Group([students[2]]))
    compare_groupings(alpha.make_grouping(course_, survey_),
                      theoretical_grouping)


def test_randomgrouper_number_of_students_in_groups() -> None:
    """Test RandomGrouper.make_group with a survey of 1 questions and a
    class of 3 students. Then check if every student is in a group."""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    students = [student1, student2, student3]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    answer1 = survey.Answer('1st')
    answer2 = survey.Answer('2nd')
    student1.set_answer(question, answer1)
    student2.set_answer(question, answer2)
    questions = [question]
    survey_ = survey.Survey(questions)
    random = grouper.RandomGrouper(2)
    grouping = random.make_grouping(course_, survey_)
    number_of_student_in_grouping = 0
    for group in grouping.get_groups():
        number_of_student_in_grouping += len(group)
    assert number_of_student_in_grouping == len(students)


def test_greedy_grouper_length_5_Students_length_3() -> None:
    """Test GreedyGrouper.make_group for groups of size 3 with 5 students"""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    students = [student1, student2, student3, student4, student5]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    answer1 = survey.Answer('1st')
    answer2 = survey.Answer('2nd')
    answer3 = survey.Answer('3rd')
    answer4 = survey.Answer('4th')
    answer5 = survey.Answer('1st')
    student1.set_answer(question, answer1)
    student2.set_answer(question, answer2)
    student3.set_answer(question, answer3)
    student4.set_answer(question, answer4)
    student5.set_answer(question, answer5)
    questions = [question]
    survey_ = survey.Survey(questions)
    greed = grouper.GreedyGrouper(3)
    greedy_grouping = greed.make_grouping(course_, survey_)
    g = grouper.Group([student1, student5, student2])
    g2 = grouper.Group([student3, student4])
    greedy_grouping_theoretical = grouper.Grouping()
    greedy_grouping_theoretical.add_group(g)
    greedy_grouping_theoretical.add_group(g2)
    compare_groupings(greedy_grouping, greedy_grouping_theoretical)


def test_sort_group_empty_survey() -> None:
    """Test GreedyGrouper._sort_group on a survey with no questions."""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    list_of_students = [student1, student2]
    survey_ = survey.Survey([])
    g = grouper.GreedyGrouper(2)
    assert g._sort_group(list_of_students, survey_).get_members() \
        == grouper.Group([student1, student2]).get_members()


def test_windowgrouper_length_5_students_length_2() -> None:
    """Test WindowGrouper.make_group for groups of size 2 with 5 students"""
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    students = [student1, student2, student3, student4, student5]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    answer1 = survey.Answer('1st')
    answer2 = survey.Answer('2nd')
    answer3 = survey.Answer('3rd')
    answer4 = survey.Answer('4th')
    answer5 = survey.Answer('1st')
    student1.set_answer(question, answer1)
    student2.set_answer(question, answer2)
    student3.set_answer(question, answer3)
    student4.set_answer(question, answer4)
    student5.set_answer(question, answer5)
    questions = [question]
    survey_ = survey.Survey(questions)
    window = grouper.WindowGrouper(2)
    window_grouping = window.make_grouping(course_, survey_)
    g = grouper.Group([student1, student2])
    g2 = grouper.Group([student3, student4])
    g3 = grouper.Group([student5])
    window_grouping_theoretical = grouper.Grouping()
    window_grouping_theoretical.add_group(g)
    window_grouping_theoretical.add_group(g2)
    window_grouping_theoretical.add_group(g3)
    compare_groupings(window_grouping, window_grouping_theoretical)


def test_windowgrouper_compare_last_first() -> None:
    """Test WindowGrouper.make_group for groups of size 2 with 5 students.
    The algorithm must compare the last student with the first
    """
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    students = [student1, student2, student3, student4, student5]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    answer1 = survey.Answer('1st')
    answer2 = survey.Answer('3rd')
    answer3 = survey.Answer('3rd')
    answer4 = survey.Answer('4th')
    answer5 = survey.Answer('4th')
    student1.set_answer(question, answer1)
    student2.set_answer(question, answer2)
    student3.set_answer(question, answer3)
    student4.set_answer(question, answer4)
    student5.set_answer(question, answer5)
    questions = [question]
    survey_ = survey.Survey(questions)
    window = grouper.WindowGrouper(2)
    window_grouping = window.make_grouping(course_, survey_)
    g = grouper.Group([student2, student3])
    g2 = grouper.Group([student4, student5])
    g3 = grouper.Group([student1])
    window_grouping_theoretical = grouper.Grouping()
    window_grouping_theoretical.add_group(g)
    window_grouping_theoretical.add_group(g2)
    window_grouping_theoretical.add_group(g3)
    compare_groupings(window_grouping, window_grouping_theoretical)


def test_windowgrouper_compare_last_first_invalid_answer() -> None:
    """Test WindowGrouper.make_group for groups of size 2 with 5 students.
    The algorithm must compare the last student with the first. Two students has
    invalid answers.
    """
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    students = [student1, student2, student3, student4, student5]
    course_ = Course('CSC148')
    course_.enroll_students(students)
    question = survey.MultipleChoiceQuestion(1, 'Which year are you in?',
                                             ['1st', '2nd', '3rd', '4th',
                                              'past 4th'])
    answer1 = survey.Answer('1st')
    answer2 = survey.Answer('3rd')
    answer3 = survey.Answer('3rd')
    answer4 = survey.Answer('41th')
    answer5 = survey.Answer('41th')
    student1.set_answer(question, answer1)
    student2.set_answer(question, answer2)
    student3.set_answer(question, answer3)
    student4.set_answer(question, answer4)
    student5.set_answer(question, answer5)
    questions = [question]
    survey_ = survey.Survey(questions)
    window = grouper.WindowGrouper(2)
    window_grouping = window.make_grouping(course_, survey_)
    g = grouper.Group([student2, student3])
    g2 = grouper.Group([student1, student4])
    g3 = grouper.Group([student5])
    window_grouping_theoretical = grouper.Grouping()
    window_grouping_theoretical.add_group(g)
    window_grouping_theoretical.add_group(g2)
    window_grouping_theoretical.add_group(g3)
    compare_groupings(window_grouping, window_grouping_theoretical)


def test_grouping_add_group_multiple_groups() -> None:
    """Test Grouping.add_group for 3 separate groups"""
    grouping = grouper.Grouping()
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    group1 = grouper.Group([student1, student2])
    group2 = grouper.Group([student3, student4])
    group3 = grouper.Group([student5])
    assert grouping.add_group(group1)
    assert grouping.add_group(group2)
    assert grouping.add_group(group3)
    assert grouping.get_groups() == [group1, group2, group3]


def test_grouping_add_group_empty_member() -> None:
    """Test Grouping.add_group for 3 separate groups. One group has no
    members"""
    grouping = grouper.Grouping()
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    group1 = grouper.Group([])
    group2 = grouper.Group([student3, student4])
    group3 = grouper.Group([student5])
    assert not grouping.add_group(group1)
    assert grouping.add_group(group2)
    assert grouping.add_group(group3)
    assert grouping.get_groups() == [group2, group3]


def test_grouping_get_groups_one_group() -> None:
    """Test Grouping.get_groups for 1 single group"""
    grouping = grouper.Grouping()
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    group1 = grouper.Group([student1, student2, student3, student4, student5])
    grouping.add_group(group1)
    assert grouping.get_groups() == [group1]


def test_grouping_get_groups_multiple_groups() -> None:
    """Test Grouping.get_groups for 3 groups"""
    grouping = grouper.Grouping()
    student1 = Student(1, 'Jack')
    student2 = Student(2, 'Mike')
    student3 = Student(3, 'Kevin')
    student4 = Student(4, 'Kelvin')
    student5 = Student(5, 'Calvin')
    group1 = grouper.Group([student1, student2])
    group2 = grouper.Group([student3, student4])
    group3 = grouper.Group([student5])
    grouping.add_group(group1)
    grouping.add_group(group2)
    grouping.add_group(group3)
    assert grouping.get_groups() == [group1, group2, group3]


def test_grouping_get_groups_empty_grouping() -> None:
    """Test Grouping.get_groups for grouping with no groups"""
    grouping = grouper.Grouping()
    assert grouping.get_groups() == []


def test_grouping_len() -> None:
    a = Student(1, 'test')
    b = Student(2, 'test2')
    e = Student(3, 'test')
    f = Student(4, 'test2')
    c = grouper.Group([a, b])
    d = grouper.Group([e, f])
    z = grouper.Grouping()
    assert len(z) == 0
    z.add_group(c)
    z.add_group(c)
    z.add_group(d)
    assert len(z) == 2


def test_grouping_str() -> None:
    a = Student(1, 'test')
    b = Student(2, 'test2')
    e = Student(3, 'test')
    f = Student(4, 'test2')
    c = grouper.Group([a, b])
    d = grouper.Group([e, f])
    z = grouper.Grouping()
    z.add_group(c)
    z.add_group(d)
    assert str(z) == 'Names: test, test2\nNames: test, test2'


def test_grouping_add_group() -> None:
    a = Student(1, 'test')
    b = Student(2, 'test2')
    e = Student(3, 'test')
    f = Student(4, 'test2')
    c = grouper.Group([a, b])
    d = grouper.Group([e, f])
    z = grouper.Grouping()
    z.add_group(c)
    z.add_group(d)
    z.add_group(d)
    assert z.get_groups() == [c, d]


def test_group_len() -> None:
    a = Student(1, 'test')
    b = Student(2, 'test2')
    c = grouper.Group([a, b])
    d = grouper.Group([])
    assert len(c) == 2
    assert len(d) == 0


def test_group_contains() -> None:
    a = Student(1, 'test')
    b = Student(2, 'test2')
    c = grouper.Group([a, b])
    d = grouper.Group([])
    e = Student(1, 'test')
    assert e in c
    assert e not in d
    assert a in c


def test_group_str() -> None:
    a = Student(1, 'test')
    b = Student(2, 'test2')
    c = grouper.Group([a, b])
    d = grouper.Group([])
    assert str(c) == "Names: test, test2"
    assert str(d) == "Names: "


def test_group_get_members() -> None:
    a = Student(1, 'test')
    b = Student(2, 'test2')
    c = grouper.Group([a, b])
    d = grouper.Group([])
    assert c.get_members() == c._members
    assert d.get_members() == d._members
    assert id(c.get_members()) != id(c._members)
    assert id(d.get_members()) != id(d._members)


def test_multiple_choice_question_str() -> None:
    f = survey.MultipleChoiceQuestion(1, 'test', ['a', 'b'])
    assert str(f) == "test: ['a', 'b']"


def test_multiple_choice_question_validate_ans() -> None:
    f = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    a = survey.Answer('a')
    b = survey.Answer('True')
    c = survey.Answer('4')
    d = survey.Answer(True)
    e = survey.Answer(4)
    g = survey.Answer(['a', 'True', '4'])
    assert f.validate_answer(a)
    assert f.validate_answer(b)
    assert f.validate_answer(c)
    assert not f.validate_answer(d)
    assert not f.validate_answer(e)
    assert not f.validate_answer(g)


def test_multiple_choice_question_similarity() -> None:
    f = survey.MultipleChoiceQuestion(1, 'test', ['a', 'b'])
    a = survey.Answer('a')
    b = survey.Answer('b')
    c = survey.Answer('a')
    assert f.get_similarity(a, b) == 0.0
    assert f.get_similarity(a, c) == 1.0


def test_numeric_question_str() -> None:
    f = survey.NumericQuestion(1, 'test', 0, 4)
    assert str(f) == "test: 0 to 4"


def test_numeric_question_validate_ans() -> None:
    f = survey.NumericQuestion(1, 'test', 0, 4)
    a = survey.Answer(0)
    b = survey.Answer(1)
    c = survey.Answer(4)
    h = survey.Answer(4.0)
    d = survey.Answer(True)
    e = survey.Answer('4')
    g = survey.Answer(['0', '4'])
    assert f.validate_answer(a)
    assert f.validate_answer(b)
    assert f.validate_answer(c)
    assert f.validate_answer(d)
    assert not f.validate_answer(h)
    assert not f.validate_answer(e)
    assert not f.validate_answer(g)


def test_numeric_question_similarity() -> None:
    f = survey.NumericQuestion(1, 'test', 0, 4)
    a = survey.Answer(0)
    b = survey.Answer(1)
    c = survey.Answer(3)
    d = survey.Answer(4)
    assert f.get_similarity(a, a) == 1.0
    assert f.get_similarity(a, b) == 0.75
    assert f.get_similarity(a, c) == 0.25
    assert f.get_similarity(a, d) == 0.0
    assert f.get_similarity(b, c) == 0.5
    assert f.get_similarity(b, d) == 0.25
    assert f.get_similarity(c, d) == 0.75


def test_yesno_question_str() -> None:
    f = survey.YesNoQuestion(1, 'test')
    assert str(f) == "test: True or False"


def test_yesno_question_validate_ans() -> None:
    f = survey.YesNoQuestion(1, 'test')
    a = survey.Answer(0)
    b = survey.Answer(1)
    c = survey.Answer(4)
    d = survey.Answer(True)
    h = survey.Answer(False)
    e = survey.Answer('4')
    g = survey.Answer(['0', '4'])
    assert not f.validate_answer(a)
    assert not f.validate_answer(b)
    assert not f.validate_answer(c)
    assert f.validate_answer(d)
    assert f.validate_answer(h)
    assert not f.validate_answer(e)
    assert not f.validate_answer(g)


def test_yesno_question_similarity() -> None:
    f = survey.YesNoQuestion(1, 'test')
    a = survey.Answer(True)
    b = survey.Answer(False)
    assert f.get_similarity(a, a) == 1.0
    assert f.get_similarity(a, b) == 0.0
    assert f.get_similarity(b, b) == 1.0


def test_checkbox_question_str() -> None:
    f = survey.CheckboxQuestion(1, 'test', ['a', 'b'])
    assert str(f) == "test: ['a', 'b']"


def test_checkbox_question_validate_ans() -> None:
    f = survey.CheckboxQuestion(1, 'test', ['a', 'True', '4'])
    a = survey.Answer('a')
    b = survey.Answer('True')
    c = survey.Answer('4')
    d = survey.Answer(True)
    e = survey.Answer(4)
    g = survey.Answer(['a', 'True', '4'])
    h = survey.Answer(['a', 'True'])
    i = survey.Answer([])
    j = survey.Answer(['a', 'True', 't'])
    k = survey.Answer(['a', 'True', 'True', '4'])
    assert not f.validate_answer(a)
    assert not f.validate_answer(b)
    assert not f.validate_answer(c)
    assert not f.validate_answer(d)
    assert not f.validate_answer(e)
    assert f.validate_answer(g)
    assert f.validate_answer(h)
    assert not f.validate_answer(i)
    assert not f.validate_answer(j)
    assert not f.validate_answer(k)


def test_checkbox_question_similarity() -> None:
    f = survey.CheckboxQuestion(1, 'test', ['a', 'b', 'c', 'd'])
    a = survey.Answer(['a'])
    b = survey.Answer(['b'])
    c = survey.Answer(['a', 'b'])
    d = survey.Answer(['c', 'b'])
    e = survey.Answer(['a', 'c', 'b'])
    g = survey.Answer(['c', 'd', 'b'])
    assert f.get_similarity(a, b) == 0.0
    assert f.get_similarity(a, c) == 0.5
    assert f.get_similarity(a, e) == 1 / 3
    assert f.get_similarity(d, e) == 2 / 3
    assert f.get_similarity(e, g) == 0.5
    assert f.get_similarity(e, e) == 1.0


def test_answer_all_questions() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(1, 'test', 0, 4)
    c = survey.YesNoQuestion(1, 'test')
    d = survey.CheckboxQuestion(1, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Answer('a')
    f = survey.Answer('e')
    g = survey.Answer(4)
    h = survey.Answer(5)
    i = survey.Answer(True)
    j = survey.Answer(False)
    k = survey.Answer(['a', 'b'])
    l = survey.Answer(['a', 'b', 'b'])
    assert e.is_valid(a)
    assert not f.is_valid(a)
    assert g.is_valid(b)
    assert not h.is_valid(b)
    assert i.is_valid(c)
    assert j.is_valid(c)
    assert k.is_valid(d)
    assert not l.is_valid(d)


def test_survey_len() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Survey([a, b, c, d])
    assert len(e) == 4


def test_survey_contains() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])
    f = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])
    g = survey.CheckboxQuestion(5, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Survey([a, b, c, d])
    assert f in e
    assert g not in e


def test_survey_str() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Survey([a, b, c, d])
    assert str(e) == "Questions:test: ['a', 'True', '4']\n"'test: 0 to 4\n' \
                     'test: True or False\n' \
                     "test: ['a', 'b', 'c', 'd']"


def test_survey_get_questions() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Survey([a, b, c, d])
    assert e.get_questions() == [a, b, c, d]


def test_survey_get_criterion() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Survey([a, b, c, d])
    assert e._get_criterion(a) == e._default_criterion
    e.set_criterion(HeterogeneousCriterion(), a)
    assert e._get_criterion(a) == e._criteria[a.id]
    e = survey.Survey([a, b, c, d])
    assert e._get_criterion(b) == e._default_criterion


def test_survey_get_weight() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Survey([a, b, c, d])
    assert e._get_weight(a) == e._default_weight
    e.set_weight(3, a)
    assert e._get_weight(a) == 3
    e = survey.Survey([a, b, c, d])
    assert e._get_weight(b) == e._default_weight


def test_survey_set_weight() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])
    f = survey.YesNoQuestion(5, 'test')

    e = survey.Survey([a, b, c, d])
    assert e.set_weight(3, a)
    assert e._weights[a.id] == 3
    assert not e.set_weight(3, f)
    assert e.set_weight(4, b)
    assert e._weights[b.id] == 4


def test_survey_set_criterion() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])
    f = survey.YesNoQuestion(5, 'test')

    e = survey.Survey([a, b, c, d])
    assert e.set_criterion(LonelyMemberCriterion(), a)
    assert e._get_criterion(a) == e._criteria[a.id]
    assert not e.set_criterion(LonelyMemberCriterion(), f)
    assert e.set_criterion(HeterogeneousCriterion(), b)
    assert e._get_criterion(b) == e._criteria[b.id]


def test_survey_score_students() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Survey([a, b, c, d])
    test = survey.Survey([])

    e.set_criterion(LonelyMemberCriterion(), a)
    e.set_criterion(HeterogeneousCriterion(), b)
    e.set_criterion(HomogeneousCriterion(), c)
    e.set_criterion(LonelyMemberCriterion(), d)
    e.set_weight(2, a)
    e.set_weight(3, b)
    e.set_weight(2, d)

    ans_1 = survey.Answer('a')
    ans_2 = survey.Answer(3)
    ans_3 = survey.Answer(True)
    ans_4 = survey.Answer(['a'])

    stu_1 = Student(1, 'test')
    stu_1.set_answer(a, ans_1)
    stu_1.set_answer(b, ans_2)
    stu_1.set_answer(c, ans_3)
    stu_1.set_answer(d, ans_4)

    stu_2 = Student(2, 'test2')
    stu_2.set_answer(a, ans_1)
    stu_2.set_answer(b, ans_2)
    stu_2.set_answer(c, ans_3)
    stu_2.set_answer(d, ans_4)
    group = [stu_1, stu_2]

    assert test.score_students(group) == 0.0
    assert e.score_students(group) == 1.25


def test_survey_score_grouping() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    e = survey.Survey([a, b, c, d])
    test = survey.Survey([])

    e.set_criterion(LonelyMemberCriterion(), a)
    e.set_criterion(HeterogeneousCriterion(), b)
    e.set_criterion(HomogeneousCriterion(), c)
    e.set_criterion(LonelyMemberCriterion(), d)
    e.set_weight(2, a)
    e.set_weight(3, b)
    e.set_weight(2, d)

    ans_1 = survey.Answer('a')
    ans_2 = survey.Answer(3)
    ans_3 = survey.Answer(True)
    ans_4 = survey.Answer(['a'])
    ans_5 = survey.Answer('4')

    stu_1 = Student(1, 'test')
    stu_1.set_answer(a, ans_1)
    stu_1.set_answer(b, ans_2)
    stu_1.set_answer(c, ans_3)
    stu_1.set_answer(d, ans_4)

    stu_2 = Student(2, 'test2')
    stu_2.set_answer(a, ans_1)
    stu_2.set_answer(b, ans_2)
    stu_2.set_answer(c, ans_3)
    stu_2.set_answer(d, ans_4)

    stu_3 = Student(3, 'test3')
    stu_3.set_answer(a, ans_5)
    stu_3.set_answer(b, ans_2)
    stu_3.set_answer(c, ans_3)
    stu_3.set_answer(d, ans_4)

    stu_4 = Student(4, 'test4')
    stu_4.set_answer(a, ans_1)
    stu_4.set_answer(b, ans_2)
    stu_4.set_answer(c, ans_3)
    stu_4.set_answer(d, ans_4)

    group = [stu_1, stu_2]
    group_2 = [stu_3, stu_4]

    new_group = grouper.Group(group)
    new_group_2 = grouper.Group(group_2)
    new_grouping = grouper.Grouping()
    new_grouping.add_group(new_group)
    new_grouping.add_group(new_group_2)

    assert test.score_students(group) == 0.0
    assert e.score_students(group) == 1.25
    assert e.score_students(group_2) == 0.75
    assert e.score_grouping(new_grouping) == 1.0


def test_homo_score_answers() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    homo_crit = HomogeneousCriterion()

    ans_1 = survey.Answer('a')
    ans_2 = survey.Answer('F')
    corr_ans_1 = survey.Answer('4')
    ans_group_1 = [ans_1, ans_2]
    ans_group_5 = [ans_1]
    correct_ans_5 = [ans_1, corr_ans_1]
    correct_ans = [ans_1, ans_1, ans_1]
    correct_ans_2 = [ans_1, ans_1, ans_1, corr_ans_1]

    ans_3 = survey.Answer(0)
    ans_4 = survey.Answer(5)
    corr_ans_2 = survey.Answer(4)
    ans_group_2 = [ans_3, ans_4]
    ans_group_6 = [ans_3]
    correct_ans_6 = [ans_3, corr_ans_2]
    correct_ans_3 = [ans_3, ans_3, ans_3]
    correct_ans_4 = [ans_3, ans_3, ans_3, corr_ans_2]

    ans_5 = survey.Answer(True)
    ans_6 = survey.Answer('F')
    corr_ans_3 = survey.Answer(False)
    ans_group_3 = [ans_5, ans_6]
    ans_group_7 = [ans_5]
    correct_ans_12 = [ans_5, corr_ans_3]
    correct_ans_9 = [ans_5, ans_5, ans_5]
    correct_ans_10 = [ans_5, ans_5, ans_5, corr_ans_3]

    ans_7 = survey.Answer(['a'])
    ans_8 = survey.Answer(['F'])
    corr_ans_4 = survey.Answer(['a', 'b', 'c'])
    ans_group_4 = [ans_7, ans_8]
    ans_group_8 = [ans_7]
    correct_ans_11 = [ans_7, corr_ans_4]
    correct_ans_7 = [ans_7, ans_7, ans_7]
    correct_ans_8 = [ans_7, ans_7, ans_7, corr_ans_4]

    with pytest.raises(InvalidAnswerError):
        homo_crit.score_answers(a, ans_group_1)
    with pytest.raises(InvalidAnswerError):
        homo_crit.score_answers(b, ans_group_2)
    with pytest.raises(InvalidAnswerError):
        homo_crit.score_answers(c, ans_group_3)
    with pytest.raises(InvalidAnswerError):
        homo_crit.score_answers(d, ans_group_4)

    assert homo_crit.score_answers(a, ans_group_5) == 1.0
    assert homo_crit.score_answers(b, ans_group_6) == 1.0
    assert homo_crit.score_answers(c, ans_group_7) == 1.0
    assert homo_crit.score_answers(d, ans_group_8) == 1.0

    assert homo_crit.score_answers(a, correct_ans) == 1.0
    assert homo_crit.score_answers(a, correct_ans_2) == 0.5
    assert homo_crit.score_answers(b, correct_ans_3) == 1.0
    assert homo_crit.score_answers(b, correct_ans_4) == 0.5
    assert homo_crit.score_answers(a, correct_ans_5) == 0.0
    assert homo_crit.score_answers(b, correct_ans_6) == 0.0
    assert homo_crit.score_answers(c, correct_ans_12) == 0.0
    assert homo_crit.score_answers(c, correct_ans_9) == 1.0
    assert homo_crit.score_answers(c, correct_ans_10) == 0.5
    assert homo_crit.score_answers(d, correct_ans_11) == 1 / 3
    assert homo_crit.score_answers(d, correct_ans_7) == 1.0
    assert homo_crit.score_answers(d, correct_ans_8) == 4 / 6


def test_heter_score_answers() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    heter_crit = HeterogeneousCriterion()

    ans_1 = survey.Answer('a')
    ans_2 = survey.Answer('F')
    corr_ans_1 = survey.Answer('4')
    ans_group_1 = [ans_1, ans_2]
    ans_group_5 = [ans_1]
    correct_ans_5 = [ans_1, corr_ans_1]
    correct_ans = [ans_1, ans_1, ans_1]
    correct_ans_2 = [ans_1, ans_1, ans_1, corr_ans_1]

    ans_3 = survey.Answer(0)
    ans_4 = survey.Answer(5)
    corr_ans_2 = survey.Answer(4)
    ans_group_2 = [ans_3, ans_4]
    ans_group_6 = [ans_3]
    correct_ans_6 = [ans_3, corr_ans_2]
    correct_ans_3 = [ans_3, ans_3, ans_3]
    correct_ans_4 = [ans_3, ans_3, ans_3, corr_ans_2]

    ans_5 = survey.Answer(True)
    ans_6 = survey.Answer('F')
    corr_ans_3 = survey.Answer(False)
    ans_group_3 = [ans_5, ans_6]
    ans_group_7 = [ans_5]
    correct_ans_12 = [ans_5, corr_ans_3]
    correct_ans_9 = [ans_5, ans_5, ans_5]
    correct_ans_10 = [ans_5, ans_5, ans_5, corr_ans_3]

    ans_7 = survey.Answer(['a'])
    ans_8 = survey.Answer(['F'])
    corr_ans_4 = survey.Answer(['a', 'b', 'c'])
    ans_group_4 = [ans_7, ans_8]
    ans_group_8 = [ans_7]
    correct_ans_11 = [ans_7, corr_ans_4]
    correct_ans_7 = [ans_7, ans_7, ans_7]
    correct_ans_8 = [ans_7, ans_7, ans_7, corr_ans_4]

    with pytest.raises(InvalidAnswerError):
        heter_crit.score_answers(a, ans_group_1)
    with pytest.raises(InvalidAnswerError):
        heter_crit.score_answers(b, ans_group_2)
    with pytest.raises(InvalidAnswerError):
        heter_crit.score_answers(c, ans_group_3)
    with pytest.raises(InvalidAnswerError):
        heter_crit.score_answers(d, ans_group_4)

    assert heter_crit.score_answers(a, ans_group_5) == 0.0
    assert heter_crit.score_answers(b, ans_group_6) == 0.0
    assert heter_crit.score_answers(c, ans_group_7) == 0.0
    assert heter_crit.score_answers(d, ans_group_8) == 0.0

    assert heter_crit.score_answers(a, correct_ans) == 0.0
    assert heter_crit.score_answers(a, correct_ans_2) == 0.5
    assert heter_crit.score_answers(b, correct_ans_3) == 0.0
    assert heter_crit.score_answers(b, correct_ans_4) == 0.5
    assert heter_crit.score_answers(a, correct_ans_5) == 1.0
    assert heter_crit.score_answers(b, correct_ans_6) == 1.0
    assert heter_crit.score_answers(c, correct_ans_12) == 1.0
    assert heter_crit.score_answers(c, correct_ans_9) == 0.0
    assert heter_crit.score_answers(c, correct_ans_10) == 0.5
    assert heter_crit.score_answers(d, correct_ans_11) == 1 - 1 / 3
    assert heter_crit.score_answers(d, correct_ans_7) == 0.0
    assert heter_crit.score_answers(d, correct_ans_8) == 1 - 2 / 3


def test_lonely_score_answers() -> None:
    a = survey.MultipleChoiceQuestion(1, 'test', ['a', 'True', '4'])
    b = survey.NumericQuestion(2, 'test', 0, 4)
    c = survey.YesNoQuestion(3, 'test')
    d = survey.CheckboxQuestion(4, 'test', ['a', 'b', 'c', 'd'])

    lonely_crit = LonelyMemberCriterion()

    ans_1 = survey.Answer('a')
    ans_2 = survey.Answer('F')
    corr_ans_1 = survey.Answer('4')
    ans_group_1 = [ans_1, ans_2]
    ans_group_5 = [ans_1]
    correct_ans_5 = [ans_1, corr_ans_1]
    correct_ans = [ans_1, ans_1, ans_1]
    correct_ans_2 = [ans_1, ans_1, ans_1, corr_ans_1]

    ans_3 = survey.Answer(0)
    ans_4 = survey.Answer(5)
    corr_ans_2 = survey.Answer(4)
    ans_group_2 = [ans_3, ans_4]
    ans_group_6 = [ans_3]
    correct_ans_6 = [ans_3, corr_ans_2]
    correct_ans_3 = [ans_3, ans_3, ans_3]
    correct_ans_4 = [ans_3, ans_3, ans_3, corr_ans_2]

    ans_5 = survey.Answer(True)
    ans_6 = survey.Answer('F')
    corr_ans_3 = survey.Answer(False)
    ans_group_3 = [ans_5, ans_6]
    ans_group_7 = [ans_5]
    correct_ans_12 = [ans_5, corr_ans_3]
    correct_ans_9 = [ans_5, ans_5, ans_5]
    correct_ans_10 = [ans_5, ans_5, ans_5, corr_ans_3]

    ans_7 = survey.Answer(['a'])
    ans_8 = survey.Answer(['F'])
    corr_ans_4 = survey.Answer(['a', 'b', 'c'])
    ans_group_4 = [ans_7, ans_8]
    ans_group_8 = [ans_7]
    correct_ans_11 = [ans_7, corr_ans_4]
    correct_ans_7 = [ans_7, ans_7, ans_7]
    correct_ans_8 = [ans_7, ans_7, ans_7, corr_ans_4]

    with pytest.raises(InvalidAnswerError):
        lonely_crit.score_answers(a, ans_group_1)
    with pytest.raises(InvalidAnswerError):
        lonely_crit.score_answers(b, ans_group_2)
    with pytest.raises(InvalidAnswerError):
        lonely_crit.score_answers(c, ans_group_3)
    with pytest.raises(InvalidAnswerError):
        lonely_crit.score_answers(d, ans_group_4)

    assert lonely_crit.score_answers(a, ans_group_5) == 0.0
    assert lonely_crit.score_answers(b, ans_group_6) == 0.0
    assert lonely_crit.score_answers(c, ans_group_7) == 0.0
    assert lonely_crit.score_answers(d, ans_group_8) == 0.0

    assert lonely_crit.score_answers(a, correct_ans) == 1.0
    assert lonely_crit.score_answers(a, correct_ans_2) == 0.0
    assert lonely_crit.score_answers(b, correct_ans_3) == 1.0
    assert lonely_crit.score_answers(b, correct_ans_4) == 0.0
    assert lonely_crit.score_answers(a, correct_ans_5) == 0.0
    assert lonely_crit.score_answers(b, correct_ans_6) == 0.0
    assert lonely_crit.score_answers(c, correct_ans_12) == 0.0
    assert lonely_crit.score_answers(c, correct_ans_9) == 1.0
    assert lonely_crit.score_answers(c, correct_ans_10) == 0.0
    assert lonely_crit.score_answers(d, correct_ans_11) == 0.0
    assert lonely_crit.score_answers(d, correct_ans_7) == 1.0
    assert lonely_crit.score_answers(d, correct_ans_8) == 0.0


if __name__ == '__main__':
    import pytest

    pytest.main(['tests.py'])
