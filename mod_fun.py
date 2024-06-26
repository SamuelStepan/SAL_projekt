import tensorflow as tf
import os
import shutil
import math
from gen_funcs import gen_data
import matplotlib.pyplot as plt

def train_save_model(model, name, data, override, epochs_num):
    """
    Function that trains given model on given data and it saves the weights to given save location if the model was not already trained
    """
    path = "saves/" + name
    if(os.path.exists(path)):
        if(not override):
            return None
        else:
            try:
                shutil.rmtree(path)
                os.makedirs(path)
            except OSError:
                print("error deleting file")
    else:
        try:
            os.makedirs(path)
        except OSError:
            print("error in creating dir")
    images, labels = data
    # Create a callback that saves the model's weights while training
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=path + "/cp.ckpt", save_weights_only=True, verbose=1)
    #training of the neural network(and saving)
    history = model.fit(images, labels, epochs = epochs_num, shuffle = False, callbacks=[cp_callback], validation_split = 0.2, verbose = 0)
    return history    

def load_weights(model, save_path):
    """
    Function that loads weights to given model from given save location
    """
    #creating path like object for saving weights
    checkpoint_dir = os.path.dirname(save_path)

    latest = tf.train.latest_checkpoint(checkpoint_dir)
    model.load_weights(latest)

def show_model(model, n:int, num_data:int, class_names:list[str], save_name, override = False, num_epochs = 10):
    """Function that trains given model by given parameters, shows achieved accuracy and shows results of prediction"""
    data = gen_data(class_names, n, num_data)
    history = train_save_model(model, save_name, data, override, num_epochs)
    if(history == None):
        print("already trained")
        load_weights(model, "saves/" + save_name + "/cp.ckpt")
    else:
        plt.plot(history.history['loss'], label='Training Loss')
        plt.plot(history.history['val_loss'], label='Validation Loss')
        plt.title('Model Training History')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()
    test_images, test_labels = gen_data(class_names, n, math.floor(num_data*0.2))
    test_acc = model.evaluate(test_images,  test_labels)

    print(f"Accuracy of model: {test_acc}")
    #Now I shall show some images and the prediction of the model 1
    fig_1 = plt.figure(figsize=(10,10))
    fig_1.suptitle('Predictions of model 1')
    predictions = model.predict(test_images[:25])
    pred_indx = [tf.math.argmax(x) for x in predictions]
    for i in range(25):
        plt.subplot(5,5,i+1)
        plt.xticks([])
        plt.yticks([])
        plt.grid(False)
        plt.imshow(test_images[i])
        plt.xlabel(class_names[pred_indx[i].numpy()])
    plt.show()