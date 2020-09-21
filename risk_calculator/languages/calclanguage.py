from abc import ABCMeta, abstractmethod


class CalcLanguage(metaclass=ABCMeta):
    @property
    def submit(self):
        raise NotImplementedError

    @property
    def missingFeatureTxt(self):
        raise NotImplementedError

    @property
    def hasLabValues(self):
        raise NotImplementedError

    @property
    def notEnoughValues(self):
        raise NotImplementedError

    @property
    def outOfRangeValues(self):
        raise NotImplementedError

    @property
    def hasO2Value(self):
        raise NotImplementedError

    @abstractmethod
    def prompt_missing_feature(self, feature):
        pass

    @abstractmethod
    def get_yes(self, yes=True):
        pass

    @abstractmethod
    def get_gender(self, male=True):
        pass

    @abstractmethod
    def get_page_desc_mortality(self, labs_auc, no_labs_auc):
        pass

    @abstractmethod
    def get_page_desc_infection(self):
        pass

    @abstractmethod
    def get_oxygen_text(self):
        pass

    @abstractmethod
    def get_insert_feat(self):
        pass

    @abstractmethod
    def get_results_card_mortality(self):
        pass

    @abstractmethod
    def get_results_card_default(self):
        pass

    @abstractmethod
    def get_results_card_infection(self):
        pass

    @abstractmethod
    def get_visual_1(self):
        pass

    @abstractmethod
    def get_model_desc_mortality(self, auc, pop, pos):
        pass

    @abstractmethod
    def get_model_desc_infection(self, auc, pop, pos):
        pass

    @abstractmethod
    def get_feature_names(self):
        pass
