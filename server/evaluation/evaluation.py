from Doctor import Doctor

class Evaluator:
    def __init__(self, risk_score, num_actors_total, num_gazes, num_faces, recog_faces_list, num_unknown_faces):

        self.detection_criteria = [num_actors_total, num_gazes, num_faces]
        self.recog_faces_list = recog_faces_list
        self.num_unknown_faces = num_unknown_faces
        self.risk_score = risk_score

        self.predictions_made = None
        self.pred_num_unknown_faces = None
        self.detected_faces_list = None
        self.pred_risk_score = None

        self.authorized_users = None
        self.unauthorized_users = None

        self.Doctor = Doctor()

        self.folders = None

    def evaluate_detection(self,
                           pred_risk_score,
                           pred_num_actors_total,
                           pred_num_gazes,
                           pred_num_faces,
                           recog_faces_list,
                           pred_num_unknown_faces):
        """
        Evaluating the detections made by the three models

        :param pred_num_actors_total: Detected number of human detections
        :param pred_num_gazes: Detected number of gazes
        :param pred_num_faces: Detected number of faces
        :param recog_faces_list: list of recognized faces from the face model
        :return: list of folder names for image to be saved

        Criteria for false positive
            1. More detections of any kind that increase risk score
            2. Threat detected where there isn't any (regarding face detection mostly)

        Criteria for false negative
            1. Less detections of threats
            2. Threat exists but none detected

        Criteria for True Positive
            1. Threat detected if exists
            2. No extra or lacking detections

        Criteria for True Negative
            1. No extra or lacking detections
            2. No threat detected
        """

        self.predictions_made = [pred_num_actors_total, pred_num_gazes, pred_num_faces]
        self.detected_faces_list = recog_faces_list
        self.pred_num_unknown_faces = pred_num_unknown_faces
        self.pred_risk_score = pred_risk_score

        self.folders = []

        self.recall_evaluation()

    def recall_evaluation(self):
        if self.risk_score < self.pred_risk_score:
            for i in range(len(self.predictions_made)):
                if self.predictions_made[i] > self.detection_criteria[i]:
                    self.folders.append('fp')

                elif self.predictions_made[i] < self.detection_criteria[i]:
                    self.folders.append('fn')

                if self.predictions_made[i] == self.detection_criteria[i]:
                    self.folders.append('tp')

                if self.predictions_made[i] == self.detection_criteria[i]:
                    self.folders.append('tn')
    #
    # def evaluate_faces(self):
    #     """
    #     :return: array
    #     """
    #     evaluations = []
    #     if self.num_unknown_faces < self.pred_num_unknown_faces:
    #         evaluations.append('fp')
    #     elif self.num_unknown_faces > self.pred_num_unknown_faces:
    #         evaluations.append('fn')
    #     elif 0 < self.num_unknown_faces == self.pred_num_unknown_faces:
    #         evaluations.append('tp')
    #     elif 0 == self.num_unknown_faces == self.pred_num_unknown_faces:
    #         evaluations.append('tn')
    #
    #
    #     for i in range(len(self.detected_faces_list)):
    #         if self.detected_faces_list[i] not in self.recog_faces_list:
    #             if self.detected_faces_list[i] in self.authorized_users:
    #                 evaluations.append('fn')
    #             elif self.detected_faces_list[i] in self.unauthorized_users:
    #                 evaluations.append('fp')






