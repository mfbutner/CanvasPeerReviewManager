from peer_reviewer_program.student import Student

import statistics


class Statistics:
    def __init__(self, s: Student, rubric):
        self.student = s
        self.rubric = rubric
        self.criteria_points = []
        try:
            self.total_points = rubric.points_possible
        except:
            pass
        self.received_criteria_scores = []
        self.received_criteria_scores_percentage = []
        self.received_criteria_scores_average = []
        self.received_criteria_scores_average_percentage = []
        self.received_criteria_scores_std = []
        self.received_criteria_scores_std_percentage = []
        self.criteria_disagreements = []
        self.criteria_disagreements_percentage = []
        self.criteria_disagreement_average = []
        self.criteria_disagreement_average_percentage = []
        self.criteria_disagreement_std = []
        self.criteria_disagreement_std_percentage = []
        self.received_total_scores = []
        self.received_total_scores_percentage = []
        self.received_total_scores_average = None
        self.received_total_scores_average_percentage = None
        self.received_total_scores_std = None
        self.received_total_scores_std_percentage = None
        self.total_disagreements = []
        self.total_disagreements_percentage = []
        self.total_disagreement_average = None
        self.total_disagreement_average_percentage = None
        self.total_disagreement_std = None
        self.total_disagreement_std_percentage = None
        self.criteria = self.pack_criteria()
        self.received_statistics = self.calculate_received_statistics()
        self.reviewer_statistics = self.calculate_reviewer_statistics()
        self.calculate_criteria_stats()
        self.calculate_total_stats()

    def pack_criteria(self):
        criteria = []
        try:
            for c in self.rubric.criteria:
                self.received_criteria_scores.append([])
                criteria.append(c['description'])
                self.criteria_points.append(c['points'])

            return criteria
        except AttributeError:
            return None

    def calculate_received_statistics(self):
        if not self.rubric:
            return
        statistic = []
        scores = []
        overall = []
        j = 0
        for review in self.student.peer_reviews_received:
            i = 0
            if review.work_flow == "completed":

                overall.append(review.given_score)
                for criteria in review.assessment['data']:
                    self.received_criteria_scores[i].append(criteria['points'])
                    if j == 0:
                        scores.append([])
                    scores[i].append(criteria['points'])
                    i = i + 1
                j = j + 1

        self.received_total_scores = overall

        if self.received_total_scores:
            statistic.append({})
            statistic[0] = {"criteria": "overall",
                            "mean": statistics.mean(overall),
                            "median": statistics.median(overall)
                            }
            if len(overall) > 1:
                statistic[0]["standard deviation"] = statistics.stdev(overall)
            else:
                statistic[0]["standard deviation"] = "not enough data points"

        i = 1
        if self.received_criteria_scores:
            for criteria in self.rubric.criteria:
                statistic.append({})
                if scores:

                    statistic[i] = {"criteria": criteria['description'],
                                    "mean": statistics.mean(scores[i - 1]),
                                    "median": statistics.median(scores[i - 1])
                                    }
                    if len(scores[i - 1]) > 1:
                        statistic[i]["standard deviation"] = statistics.stdev(scores[i - 1])
                    else:
                        statistic[i]["standard deviation"] = "not enough data points"
                    i = i + 1
                else:
                    return "no data points"
            return statistic
        #
        # pass

    def calculate_reviewer_statistics(self):
        if not self.rubric:
            return
        statistic = []
        scores = []
        overall = []
        j = 0
        for review in self.student.peer_reviews:
            i = 0
            if review.work_flow == "completed":
                overall.append(review.given_score)

                for criteria in review.assessment['data']:
                    if j == 0:
                        scores.append([])
                    scores[i].append(criteria['points'])
                    i = i + 1
                j = j + 1

        if overall:
            statistic.append({})
            statistic[0] = {"criteria": "overall",
                            "mean": statistics.mean(overall),
                            "median": statistics.median(overall)
                            }
            if len(overall) > 1:
                statistic[0]["standard deviation"] = statistics.stdev(overall)
            else:
                statistic[0]["standard deviation"] = "not enough data points"

        i = 1
        if self.rubric:
            for criteria in self.rubric.criteria:
                statistic.append({})
                if scores:

                    statistic[i] = {"criteria": criteria['description'],
                                    "mean": statistics.mean(scores[i - 1]),
                                    "median": statistics.median(scores[i - 1])
                                    }
                    if len(scores[i - 1]) > 1:
                        statistic[i]["standard deviation"] = statistics.stdev(scores[i - 1])
                    else:
                        statistic[i]["standard deviation"] = "not enough data points"
                    i = i + 1
                else:
                    return "no data points"
            return statistic

        pass

    def calculate_criteria_stats(self):
        for i in range(len(self.rubric.criteria)):
            if len(self.received_criteria_scores[i]):
                self.received_criteria_scores_average.append(statistics.mean(self.received_criteria_scores[i]))
                self.received_criteria_scores_average_percentage.append("{:.2%}".format(statistics.mean
                                                                                        (self.received_criteria_scores[
                                                                                             i]) /
                                                                                        self.criteria_points[i]))
                self.received_criteria_scores_percentage.append(["{:.2%}".format(score /
                                                                                 self.criteria_points[i]) for score in
                                                                 self.received_criteria_scores[i]])
                if len(self.received_criteria_scores[i]) > 1:
                    self.criteria_disagreements.append([statistics.fabs(score -
                                                                        (self.received_criteria_scores_average[i] * len(
                                                                            self.received_criteria_scores[i]) - score) /
                                                                        (len(self.received_criteria_scores[i]) - 1))
                                                        for score in self.received_criteria_scores[i]])
                    self.criteria_disagreements_percentage.append(["{:.2%}".format(statistics.fabs(score -
                                                                                                   (
                                                                                                           self.received_criteria_scores_average[
                                                                                                               i] * len(
                                                                                                       self.received_criteria_scores[
                                                                                                           i]) - score) /
                                                                                                   (len(
                                                                                                       self.received_criteria_scores[
                                                                                                           i]) - 1)) /
                                                                                   self.criteria_points[i])
                                                                   for score in self.received_criteria_scores[i]])

                    self.criteria_disagreement_average.append(statistics.mean(self.criteria_disagreements[i]))
                    self.criteria_disagreement_average_percentage.append("{:.2%}".format
                                                                         (statistics.mean(self.criteria_disagreements[i])
                                                                                          / self.criteria_points[i]))
                    self.received_criteria_scores_std.append(statistics.stdev(self.received_criteria_scores[i]))
                    self.received_criteria_scores_std_percentage.append("{:.2%}".format(statistics.stdev(
                        self.received_criteria_scores[i]) / self.criteria_points[i]))
                    self.criteria_disagreement_std.append(statistics.stdev(self.criteria_disagreements[i]))
                    self.criteria_disagreement_std_percentage.append("{:.2%}".format(
                        statistics.stdev(self.criteria_disagreements[i])
                                         / self.criteria_points[i]))

                else:
                    self.received_criteria_scores_std.append("Not Enough Data Points")
                    self.criteria_disagreements.append(
                        ["Not Enough Data Points" for score in self.received_criteria_scores[i]])
                    self.criteria_disagreement_average.append("No Data Available")
                    self.criteria_disagreement_std.append("Not Enough Data Points")
                    self.received_criteria_scores_std_percentage.append("Not Enough Data Points")
                    self.criteria_disagreements_percentage.append(
                        ["Not Enough Data Points" for score in self.received_criteria_scores[i]])
                    self.criteria_disagreement_average_percentage.append("No Data Available")
                    self.criteria_disagreement_std_percentage.append("Not Enough Data Points")
            else:
                self.received_criteria_scores.append([])
                self.criteria_disagreement_std.append("Not Enough Data Points")
                self.received_criteria_scores_average.append("No Data Available")
                self.criteria_disagreements.append([])
                self.criteria_disagreement_average.append("No Data Available")
                self.received_criteria_scores_std.append("Not Enough Data Points")
                self.received_criteria_scores_percentage.append([])
                self.criteria_disagreement_std_percentage.append("Not Enough Data Points")
                self.received_criteria_scores_average_percentage.append("No Data Available")
                self.criteria_disagreements_percentage.append([])
                self.criteria_disagreement_average_percentage.append("No Data Available")
                self.received_criteria_scores_std_percentage.append("Not Enough Data Points")
        pass

    def calculate_total_stats(self):

        if len(self.received_total_scores):
            self.received_total_scores_average = statistics.mean(self.received_total_scores)
            self.received_total_scores_average_percentage = "{:.2%}".format(statistics.mean(self.received_total_scores)
                                                                            / self.total_points)
            self.received_total_scores_percentage= (["{:.2%}".format(score / self.total_points)
                                                          for score in self.received_total_scores])

            if len(self.received_total_scores) > 1:
                self.total_disagreements = ([statistics.fabs(score -
                                                             (self.received_total_scores_average * len(
                                                                 self.received_total_scores) - score) /
                                                             (len(self.received_total_scores) - 1))
                                             for score in self.received_total_scores])
                self.total_disagreements_percentage = (["{:.2%}".format(statistics.fabs(score -
                                                                                        (
                                                                                                    self.received_total_scores_average * len(
                                                                                                self.received_total_scores) - score) /
                                                                                        (len(
                                                                                            self.received_total_scores) - 1)) / self.total_points)
                                                        for score in self.received_total_scores])
                self.total_disagreement_average = statistics.mean(self.total_disagreements)
                self.total_disagreement_average_percentage = "{:.2%}".format \
                    (statistics.mean(self.total_disagreements) / self.total_points)
                self.received_total_scores_std = statistics.stdev(self.received_total_scores)
                self.received_total_scores_std_percentage = "{:.2%}".format \
                    (statistics.stdev(self.received_total_scores) / self.total_points)
                self.total_disagreement_std = statistics.stdev(self.total_disagreements)
                self.total_disagreement_std_percentage = "{:.2%}".format\
                    (statistics.stdev(self.total_disagreements) / self.total_points)

            else:
                self.received_total_scores_std = "Not Enough Data Points"
                self.total_disagreement_std = "Not Enough Data Points"
                self.total_disagreements = ["Not Enough Data Points" for score in self.received_total_scores]
                self.total_disagreement_average = "No Data Available"
                self.received_total_scores_std_percentage = "Not Enough Data Points"
                self.total_disagreement_std_percentage = "Not Enough Data Points"
                self.total_disagreements_percentage = ["Not Enough Data Points" for score in self.received_total_scores]
                self.total_disagreement_average_percentage = "No Data Available"

        else:
            self.total_disagreement_std = "Not Enough Data Points"
            self.received_total_scores_average = "No Data Available"
            self.total_disagreements = []
            self.total_disagreement_average = "No Data Available"
            self.received_total_scores_std = "Not Enough Data Points"
            self.total_disagreement_std_percentage = "Not Enough Data Points"
            self.received_total_scores_average_percentage = "No Data Available"
            self.total_disagreements_percentage = []
            self.total_disagreement_average_percentage = "No Data Available"
            self.received_total_scores_std_percentage = "Not Enough Data Points"

        pass
