"""CSC148 Assignment 0: Sample tests

=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains sample tests for Assignment 0.

Warning: This is an extremely incomplete set of tests!
Add your own to practice writing tests and to be confident your code is correct.

Note: this file is to only help you; you will not submit it when you hand in
the assignment.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Authors: Mario Badr, Christine Murad, Diane Horton, Misha Schwartz, Sophia Huynh
and Jaisie Sin

All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Mario Badr, Christine Murad, Diane Horton, Misha Schwartz,
Sophia Huynh and Jaisie Sin
"""
from datetime import datetime
from gym import WorkoutClass, Instructor, Gym


def test_instructor_attributes() -> None:
    """Test the public attributes of a new instructor."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.get_id() == 5
    assert instructor.name == 'Matthew'
    assert instructor.get_num_certificates() == 0
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
    assert instructor.can_teach(kickboxing) is False


def test_instructor_one_certificate_get_certificates() -> None:
    """Test Instructor.get_num_certificates with a single certificate."""
    instructor = Instructor(5, 'Matthew')
    assert instructor.add_certificate('Kickboxing')
    assert instructor.get_num_certificates() == 1


def test_instructor_one_certificate_can_teach() -> None:
    """Test Instructor.can_teach with a single satisfying certificate."""
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    assert instructor.add_certificate('Lifeguard')
    assert instructor.can_teach(swimming)


def test_instructor_multiple_certificate_can_teach() -> None:
    """Test Instructor.can_teach with a single satisfying certificate."""
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard', 'test', 'tes'])
    assert instructor.add_certificate('Lifeguard')
    assert instructor.can_teach(swimming) is False
    assert instructor.add_certificate('l')
    assert instructor.can_teach(swimming) is False
    assert instructor.add_certificate('tes')
    assert instructor.can_teach(swimming) is False
    assert instructor.add_certificate('test')
    assert instructor.can_teach(swimming)
    assert instructor.get_num_certificates() == 4


def test_gym_attributes() -> None:
    """Test the public attributes of a new gym."""
    ac = Gym('Athletic Centre')
    assert ac.name == 'Athletic Centre'


def test_gym_add_instructor() -> None:
    """Test add instructor."""
    ac = Gym('Athletic Centre')
    assert ac.name == 'Athletic Centre'
    diane = Instructor(1, 'Diane')
    assert ac.add_instructor(diane)
    assert ac._instructors == {1: diane}
    assert ac.add_instructor(diane) is False
    dian1 = Instructor(2, 'Dian')
    assert ac.add_instructor(dian1)
    assert ac._instructors == {1: diane, 2: dian1}
    dia = Instructor(2, 'Dian')
    assert ac.add_instructor(dia) is False
    dian = Instructor(3, 'Dian')
    assert ac.add_instructor(dian)
    assert ac._instructors == {1: diane, 2: dian1, 3: dian}


def test_gym_add_workout_class() -> None:
    """Test add workout class."""
    ac = Gym('Athletic Centre')
    kickboxing = WorkoutClass('Kickboxing', ['Strength Training'])
    assert ac.add_workout_class(kickboxing)
    assert ac._workouts == {'Kickboxing': kickboxing}
    assert ac.add_workout_class(kickboxing) is False

    tes = WorkoutClass('test', ['test1', 'test2', 'test3'])
    assert ac.add_workout_class(tes)
    assert ac._workouts == {'Kickboxing': kickboxing, 'test': tes}
    assert ac.add_workout_class(tes) is False


def test_gym_add_room() -> None:
    """Test add room."""
    ac = Gym('Athletic Centre')
    assert ac.add_room('Dance Studio', 50)
    assert ac._rooms == {'Dance Studio': 50}
    assert ac.add_room('Dance Studio', 50) is False
    assert ac.add_room('Dance Studi', 50)
    assert ac.add_room('', 50)
    assert ac._rooms == {'Dance Studio': 50, 'Dance Studi': 50, '': 50}
    assert ac.add_room('', 50) is False


def test_schedule_workout_doctest() -> None:
    """Test schedule workout."""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert ac.add_instructor(diane)
    assert diane.add_certificate('Cardio 1')
    assert ac.add_room('Dance Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                     boot_camp.get_name(), diane.get_id())
    assert ac._schedule == {sep_9_2019_12_00: {'Dance Studio':
                                                (diane, boot_camp, [])}}


def test_schedule_workout_can_teach() -> None:
    """Test schedule workout can teach."""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert ac.add_instructor(diane)
    #  assert diane.add_certificate('Cardio 1')
    assert ac.add_room('Dance Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                     boot_camp.get_name(),
                                     diane.get_id()) is False
    assert ac._schedule == {}


def test_schedule_workout_room_available() -> None:
    """Test schedule workout can teach."""
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    assert ac.add_instructor(diane)
    test = Instructor(2, 'Diane')
    assert ac.add_instructor(test)
    assert diane.add_certificate('Cardio 1')
    assert test.add_certificate('Cardio 1')
    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Danc Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dan Studio',
                                     boot_camp.get_name(),
                                     diane.get_id()) is False
    assert ac._schedule == {}
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                     boot_camp.get_name(),
                                     diane.get_id())
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio',
                                     boot_camp.get_name(),
                                     diane.get_id()) is False
    assert ac._schedule == {sep_9_2019_12_00: {'Dance Studio':
                                                   (diane, boot_camp, [])}}
    assert ac.schedule_workout_class(datetime(2019, 9, 9, 1, 0), 'Dance Studio',
                                     boot_camp.get_name(),
                                     diane.get_id())
    assert ac.schedule_workout_class(datetime(2019, 9, 9, 1, 0), 'Danc Studio',
                                     boot_camp.get_name(),
                                     diane.get_id()) is False
    assert ac.schedule_workout_class(datetime(2019, 9, 9, 1, 0), 'Danc Studio',
                                     boot_camp.get_name(),
                                     test.get_id())
    assert ac._schedule == {sep_9_2019_12_00:
                            {'Dance Studio': (diane, boot_camp, [])},
                            datetime(2019, 9, 9, 1, 0):
                            {'Dance Studio': (diane, boot_camp, []),
                             'Danc Studio': (test, boot_camp, [])}}


def test_gym_register_everything() -> None:
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    dian = Instructor(2, 'Dian')
    assert diane.add_certificate('Cardio 1')
    assert dian.add_certificate('Cardio 1')
    assert ac.add_instructor(diane)
    assert ac.add_instructor(dian)

    assert ac.add_room('Dance Studio', 3)
    assert ac.add_room('Danc Studio', 3)

    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)

    sep_9_2019_12_00 = datetime(2019, 9, 9, 12, 0)
    sep_9_2019_13_00 = datetime(2019, 9, 9, 13, 0)
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Dance Studio', \
                                     boot_camp.get_name(), diane.get_id())
    assert ac.schedule_workout_class(sep_9_2019_12_00, 'Danc Studio', \
                                     boot_camp.get_name(), dian.get_id())

    assert ac.register(sep_9_2019_12_00, 'Philip', 'Boot Camp')
    assert ac.register(datetime(2019, 9, 9, 11, 0), 'Philip', 'Boot Camp') is False
    assert ac.register(sep_9_2019_12_00, 'Philip', 'Boot Camp') is False
    assert ac.register(sep_9_2019_12_00, 'test', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'tes', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'te', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'tes', 'Boot Camp') is False

    assert ac._schedule == {sep_9_2019_12_00:
        {'Dance Studio': (diane, boot_camp, ['Philip', 'test', 'tes']),
         'Danc Studio': (dian, boot_camp, ['te'])}}

    assert ac.register(sep_9_2019_12_00, 'ts', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 't', 'Boot Camp')
    assert ac.register(sep_9_2019_12_00, 'z', 'Boot Camp') is False
    assert ac._schedule == {sep_9_2019_12_00:
        {'Dance Studio': (diane, boot_camp, ['Philip', 'test', 'tes']),
         'Danc Studio': (dian, boot_camp, ['te', 'ts', 't'])}}

    assert ac.schedule_workout_class(sep_9_2019_13_00, 'Danc Studio', \
                                     boot_camp.get_name(), dian.get_id())
    assert ac.register(sep_9_2019_13_00, 'a', 'Boot Camp')

    assert ac._schedule == {sep_9_2019_12_00:
        {'Dance Studio': (diane, boot_camp, ['Philip', 'test', 'tes']),
         'Danc Studio': (dian, boot_camp, ['te', 'ts', 't'])},
          sep_9_2019_13_00: {'Danc Studio': (dian, boot_camp, ['a'])}}


def test_gym_register_one_class() -> None:
    """Test Gym.register with a single user and class."""
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert instructor.add_certificate('Lifeguard')
    assert ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    assert ac.register(jan_28_2020_11_00, 'Benjamin', 'Swimming')


def test_gym_offerings_everything() -> None:
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    dian = Instructor(2, 'Dian')
    dia = Instructor(3, 'Dia')

    assert diane.add_certificate('Cardio 1')
    assert dian.add_certificate('Cardio 1')
    assert dia.add_certificate('Cardio 1')

    assert ac.add_instructor(diane)
    assert ac.add_instructor(dian)
    assert ac.add_instructor(dia)

    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Danc Studio', 50)
    assert ac.add_room('Dan Studio', 50)

    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    t1 = datetime(2019, 9, 9, 12, 0)
    t2 = datetime(2019, 9, 9, 13, 0)
    assert ac.offerings_at(t1) == []
    assert ac.schedule_workout_class(t1, 'Dance Studio', \
                              boot_camp.get_name(), diane.get_id())
    assert ac.offerings_at(t1) == [('Diane', 'Boot Camp', 'Dance Studio')]
    assert ac.schedule_workout_class(t1, 'Danc Studio', \
                                     boot_camp.get_name(), dian.get_id())
    assert ac.schedule_workout_class(t1, 'Dan Studio', \
                                     boot_camp.get_name(), dia.get_id())
    assert ac.offerings_at(t1) == [('Diane', 'Boot Camp', 'Dance Studio'),
                                   ('Dian', 'Boot Camp', 'Danc Studio'),
                                   ('Dia', 'Boot Camp', 'Dan Studio'),]
    assert ac.schedule_workout_class(t2, 'Dance Studio', \
                                     boot_camp.get_name(), diane.get_id())
    assert ac.offerings_at(t2) == [('Diane', 'Boot Camp', 'Dance Studio')]


def test_gym_offerings_at_one_class() -> None:
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', ['Lifeguard'])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert instructor.add_certificate('Lifeguard')
    assert ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    assert ac.offerings_at(jan_28_2020_11_00) == \
           [('Matthew', 'Swimming', '25-yard Pool')]


def test_gym_instr_hours_everything() -> None:
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    david = Instructor(2, 'David')

    assert diane.add_certificate('Cardio 1')
    assert david.add_certificate('Cardio 1')
    assert ac.add_instructor(diane)
    assert ac.add_instructor(david)

    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Danc Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    t1 = datetime(2019, 9, 9, 12, 0)
    t2 = datetime(2019, 9, 10, 12, 0)
    t3 = datetime(2019, 9, 8, 12, 0)
    t4 = datetime(2019, 9, 11, 12, 0)

    assert ac.instructor_hours(t1, t2) == {1: 0, 2: 0}
    assert ac.schedule_workout_class(t1, 'Dance Studio', boot_camp.get_name(), 1)
    assert ac.instructor_hours(t1, t2) == {1: 1, 2: 0}
    assert ac.schedule_workout_class(t2, 'Dance Studio', boot_camp.get_name(), 2)
    assert ac.instructor_hours(t1, t2) == {1: 1, 2: 1}
    assert ac.schedule_workout_class(t3, 'Dance Studio', boot_camp.get_name(), 1)
    assert ac.schedule_workout_class(t4, 'Dance Studio', boot_camp.get_name(), 1)
    assert ac.instructor_hours(t1, t2) == {1: 1, 2: 1}

    d = Instructor(3, 'David')
    assert d.add_certificate('Cardio 1')
    assert ac.add_instructor(d)
    assert ac.schedule_workout_class(t3, 'Danc Studio', boot_camp.get_name(), 3)
    assert ac.instructor_hours(t3, t4) == {1: 3, 2: 1, 3: 1}


def test_gym_payroll_everything() -> None:
    ac = Gym('Athletic Centre')
    diane = Instructor(1, 'Diane')
    david = Instructor(2, 'David')

    assert diane.add_certificate('Cardio 1')
    assert diane.add_certificate('test')
    assert david.add_certificate('Cardio 1')
    assert ac.add_instructor(diane)
    assert ac.add_instructor(david)

    assert ac.add_room('Dance Studio', 50)
    assert ac.add_room('Danc Studio', 50)
    boot_camp = WorkoutClass('Boot Camp', ['Cardio 1'])
    assert ac.add_workout_class(boot_camp)
    t1 = datetime(2019, 9, 9, 12, 0)
    t2 = datetime(2019, 9, 10, 12, 0)
    t3 = datetime(2019, 9, 8, 12, 0)
    t4 = datetime(2019, 9, 11, 12, 0)

    assert ac.payroll(t1, t2, 25.0) == [(1, 'Diane', 0, 0.0),
                                        (2, 'David', 0, 0.0)]

    assert ac.instructor_hours(t1, t2) == {1: 0, 2: 0}
    assert ac.schedule_workout_class(t1, 'Dance Studio', boot_camp.get_name(), 1)
    assert ac.instructor_hours(t1, t2) == {1: 1, 2: 0}
    assert ac.schedule_workout_class(t2, 'Dance Studio', boot_camp.get_name(), 2)
    assert ac.instructor_hours(t1, t2) == {1: 1, 2: 1}
    assert ac.schedule_workout_class(t3, 'Dance Studio', boot_camp.get_name(), 1)
    assert ac.schedule_workout_class(t4, 'Dance Studio', boot_camp.get_name(), 1)
    assert ac.instructor_hours(t1, t2) == {1: 1, 2: 1}

    assert ac.payroll(t1, t2, 25.0) == [(1, 'Diane', 1, 28.0),
                                        (2, 'David', 1, 26.5)]
    assert diane.add_certificate('tst')
    assert diane.add_certificate('tet')
    assert ac.payroll(t1, t2, 25.0) == [(1, 'Diane', 1, 31.0),
                                        (2, 'David', 1, 26.5)]

    d = Instructor(5, 'Davi')
    assert d.add_certificate('Cardio 1')
    assert ac.add_instructor(d)
    assert ac.schedule_workout_class(t3, 'Danc Studio', boot_camp.get_name(), 5)
    assert ac.instructor_hours(t3, t4) == {1: 3, 2: 1, 5: 1}
    assert ac.payroll(t3, t4, 25.0) == [(1, 'Diane', 3, 93.0),
                                        (2, 'David', 1, 26.5),
                                        (5, 'Davi', 1, 26.5)]
    e = Instructor(4, 'Dav')
    assert e.add_certificate('Cardio 1')
    assert e.add_certificate('Cardio')
    assert ac.add_instructor(e)
    assert ac.schedule_workout_class(t4, 'Danc Studio', boot_camp.get_name(), 4)
    assert ac.payroll(t3, t4, 25.0) == [(1, 'Diane', 3, 93.0),
                                        (2, 'David', 1, 26.5),
                                        (4, 'Dav', 1, 28.0),
                                        (5, 'Davi', 1, 26.5)]

def test_gym_one_instructor_one_hour_pay_no_certificates() -> None:
    ac = Gym('Athletic Centre')
    instructor = Instructor(5, 'Matthew')
    swimming = WorkoutClass('Swimming', [])
    jan_28_2020_11_00 = datetime(2020, 1, 29, 11, 0)
    assert ac.add_workout_class(swimming)
    assert ac.add_instructor(instructor)
    assert ac.add_room('25-yard Pool', 100)
    assert ac.schedule_workout_class(jan_28_2020_11_00, '25-yard Pool',
                                     swimming.get_name(), instructor.get_id())
    t1 = datetime(2020, 1, 17, 11, 0)
    t2 = datetime(2020, 1, 29, 13, 0)
    assert ac.payroll(t1, t2, 22.0) == [(5, 'Matthew', 1, 22)]


if __name__ == '__main__':
    import pytest

    pytest.main(['a0_sample_test.py'])
