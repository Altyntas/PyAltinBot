from keras._tf_keras.keras.models import Model
from keras._tf_keras.keras.layers import Dense, Embedding, LSTM, Input
from keras._tf_keras.keras.saving import load_model
import chatbot_data as dp


enc_inp = Input(shape=(13, ))
dec_inp = Input(shape=(13, ))


VOCAB_SIZE = len(dp.vocab)
embed = Embedding(VOCAB_SIZE+1, output_dim=50, 
                  input_length=13,
                  trainable=True                  
                  )


enc_embed = embed(enc_inp)
enc_lstm = LSTM(400, return_sequences=True, return_state=True)
enc_op, h, c = enc_lstm(enc_embed)
enc_states = [h, c]



dec_embed = embed(dec_inp)
dec_lstm = LSTM(400, return_sequences=True, return_state=True)
dec_op, _, _ = dec_lstm(dec_embed, initial_state=enc_states)

dense = Dense(VOCAB_SIZE, activation='softmax')

dense_op = dense(dec_op)

model = Model([enc_inp, dec_inp], dense_op)

model.compile(loss='categorical_crossentropy',metrics=['acc'],optimizer='adam')
model.fit([dp.encoder_inp, dp.decoder_inp],dp.decoder_final_output,epochs=5)

model.save('mymodel.keras')

#На случай если нам нужно сохранять и дообучать модель
'''
loaded_model = load_model("mymodel.keras")

loaded_model.compile(loss='categorical_crossentropy',metrics=['acc'],optimizer='adam')
loaded_model.fit([dp.encoder_inp, dp.decoder_inp],dp.decoder_final_output,epochs=5)

loaded_model.save('mymodel.keras')
'''