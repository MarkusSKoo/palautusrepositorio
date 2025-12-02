class And:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if not matcher.test(player):
                return False

        return True

class Or:
    def __init__(self, *matchers):
        self._matchers = matchers

    def test(self, player):
        for matcher in self._matchers:
            if matcher.test(player):
                return True

        return False


class PlaysIn:
    def __init__(self, team):
        self._team = team

    def test(self, player):
        return player.team == self._team


class HasAtLeast:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value >= self._value

class All:
    def test(self, player):
        return True

class Not:
    def __init__(self, opposite):
        self.opposite = opposite

    def test(self, player):
        if self.opposite.test(player):
            return False
        return True

class HasFewerThan:
    def __init__(self, value, attr):
        self._value = value
        self._attr = attr

    def test(self, player):
        player_value = getattr(player, self._attr)

        return player_value < self._value

class QueryBuilder:
    def __init__(self, query = All()):
        self.query_object = query

    def combine(self, *matchers):
        return QueryBuilder(And(self.query_object, *matchers))

    def one_of(self, *builders):
        matchers = []
        for builder in builders:
            matchers.append(builder.build())
        return QueryBuilder(Or(*matchers))

    def plays_in(self, team):
        return self.combine(self.query_object, PlaysIn(team))

    def has_at_least(self, value, attr):
        return self.combine(self.query_object, HasAtLeast(value, attr))

    def has_fewer_than(self, value, attr):
        return self.combine(self.query_object, HasFewerThan(value, attr))

    def build(self):
        return self.query_object
