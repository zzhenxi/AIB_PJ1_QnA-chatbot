# 의도 분류 모듈 생성 
# 의도 분류 모델 파일을 활용해 텍스트의 의도 클래스 예측
import sys
sys.path.append('/Users/zhenxi/Desktop/for_git/AIB_PJ1/AIB_PJ1_QnA-chatbot/chatbot')

import tensorflow as tf
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing

class IntentModel:
    def __init__(self, model_name, preprocess):
        # 의도 클래스별 레이블
        self.labels = {0: "인사", 1: "욕설", 2: "주문", 3: "예약", 4: "기타"}
        # 의도 분류 모델 불러오기 
        self.model = load_model(model_name)
        # 챗봇 Preprocess 객체
        self.p = preprocess
    
    # 의도 클래스 예측
    def predict_class(self, query):
        # 형태소 분석
        pos = self.p.pos(query)
        
        # 문장 내 키워드 추출(불용어 제거)
        keywords = self.p.get_keywords(pos, without_tag=True)
        sequences = [self.p.get_wordidx_sequence(keywords)]

         # 단어 시퀀스 벡터 크기
        from config.GlobalParams import MAX_SEQ_LEN

        # 패딩 처리
        padded_seqs = preprocessing.sequence.pad_sequences(sequences, maxlen=MAX_SEQ_LEN, padding='post')

        predict = self.model.predict(padded_seqs) 
        predict_class = tf.math.argmax(predict, axis=1)
        return predict_class.numpy()[0]



'''
[note]
predict 결과 예시 
[2.8261976e-02, 5.1256761e-02, 1.3123078e-09, 7.0551470e-10, 9.2048126e-01]
여기서 값이 가장 크게 나는 class를 채택한다. (위의 결과 같은 경우, 4)
'''


