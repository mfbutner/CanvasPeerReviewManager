from student import student

import statistics


class Statistics:
    def __init__(self, s : student, rubric):
        self.student = s
        self.rubric = rubric
        self.received_statistics = self.calculate_received_statistics()
        self.reviewer_statistics = self.calculate_reviewer_statistics()

    def calculate_received_statistics(self):
        statistic = []
        scores = []
        overall = []
        j = 0
        for review in self.student.peer_reviews_received:
            i = 0
            if review.work_flow == "completed":
                overall.append(review.given_score)
                for criteria in review.assessment['data']:
                    if j == 0 :
                        scores.append([])
                    scores[i].append(criteria['points'])
                    i = i + 1
            j = j +1





        if overall :
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

        for criteria in self.rubric.criteria:
            statistic.append({})
            if scores:

                statistic[i]= {"criteria": criteria['description'],
                             "mean": statistics.mean(scores[i-1]),
                            "median": statistics.median(scores[i-1])
                            }
                if len(scores[i-1]) > 1:
                    statistic[i]["standard deviation"] = statistics.stdev(scores[i-1])
                else:
                    statistic[i]["standard deviation"] = "not enough data points"
                i = i + 1
            else:
                return "no data points"
        return statistic


        pass

    def calculate_reviewer_statistics(self):
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

