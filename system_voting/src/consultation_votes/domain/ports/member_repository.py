from abc import abstractmethod, ABC


class MemberRepository(ABC):

    @abstractmethod
    def get_by_id(self, member_id):
        pass