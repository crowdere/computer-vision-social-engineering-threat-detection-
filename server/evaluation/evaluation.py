class Evaluator:
    def __init__(self, num_actors_total, num_gazes, num_faces):
        self.num_actors_total = num_actors_total
        self.num_gazes = num_gazes
        self.num_faces = num_faces

    def evaluate_detection(self, pred_num_actors_total,
                                  predicted_num_gazes,
                                  predicted_num_faces):

        """
        Evaluating the detections made by the three models

        :param pred_num_actors_total: Detected number of human detections
        :param predicted_num_gazes: Detected number of gazes
        :param predicted_num_faces: Detected number of faces
        :return: Folder name for image to be saved
        """

        pass

    def eval_false_recognition(self, list_detected_people):
        pass

    def false_positives(self):
        pass

    def false_negatives(self):
        pass

    def true_positives(self):
        pass

    def true_negatives(self):
        pass

