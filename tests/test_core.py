from bbb.core import Participant, Vote, add_votes, count_votes


def test_can_count_votes():
    votes = (
        [Vote(participant_id=1)] * 5 + [Vote(participant_id=2)] * 13 + [Vote(participant_id=3)] * 42
    )

    assert count_votes(votes) == {1: 5, 2: 13, 3: 42}


def test_can_add_votes():
    flash = Participant(1, "The Flash", 0)
    batman = Participant(2, "Batman", 0)
    superman = Participant(3, "Superman", 0)

    votes_to_id = {1: 3, 2: 5, 3: 42}

    add_votes([flash, batman, superman], votes_to_id)

    assert flash.votes == 3
    assert batman.votes == 5
    assert superman.votes == 42
