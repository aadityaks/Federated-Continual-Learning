import pdb
import math
import random
import tensorflow as tf

from misc.utils import *
from modules.federated import ClientModule

class Client(ClientModule):
    """ FedProx Client
    Performing fedprox client algorithms 
    Created by:
        Aaditya Singh (asingh@gatech.edu)
    """
    def __init__(self, gid, args, initial_weights):
        super(Client, self).__init__(gid, args, initial_weights)
        self.state['gpu_id'] = gid

    def train_one_round(self, client_id, curr_round, selected, global_weights=None, from_kb=None):
        ######################################
        self.switch_state(client_id)
        ######################################
        self.state['round_cnt'] += 1
        self.state['curr_round'] = curr_round
        self.global_weights = global_weights
        
        if self.state['curr_task']<0:
            self.init_new_task()
            self.set_weights(global_weights) 
        else:
            is_last_task = (self.state['curr_task']==self.args.num_tasks-1)
            is_last_round = (self.state['round_cnt']%self.args.num_rounds==0 and self.state['round_cnt']!=0)
            if is_last_round:
                if is_last_task:
                    if self.train.state['early_stop']:
                        self.train.evaluate()
                    self.stop()
                    return
                else:
                    self.init_new_task()
                    self.state['prev_body_weights'] = self.nets.get_body_weights(self.state['curr_task'])
            else:
                self.load_data()

        if selected:
            self.set_weights(global_weights)

        with tf.device('/device:GPU:{}'.format(self.state['gpu_id'])):
            self.train.train_one_round(self.state['curr_round'], self.state['round_cnt'], self.state['curr_task'])
        
        self.logger.save_current_state(self.state['client_id'], {
            'scores': self.train.get_scores(),
            'capacity': self.train.get_capacity(),
            'communication': self.train.get_communication()
        })
        self.save_state()
        
        if selected:
            return self.get_weights(), self.get_train_size()

    def loss(self, y_true, y_pred):
        # real loss
        local_weight = self.get_weights()
        global_weight = self.global_weights
        loss = tf.keras.losses.categorical_crossentropy(y_true, y_pred)
        proximal_loss = 0
        for lid in range(len(local_weight)):
            layer_diff = local_weight[lid]-global_weight[lid]
            proximal_loss += self.args.mu * tf.nn.l2_loss(layer_diff)
        
        # px_fn_loss = self.proximal_term(local_weight, global_weight, self.args.mu)
        loss += proximal_loss
        return loss

    def proximal_term(self, local_model, global_model, mu):
        """Proximal regularizer of FedProx"""

        vec = []
        for _, (param1, param2) in enumerate(zip(local_model, global_model)):
            val = tf.reshape((param1 - param2), [-1, 1])
            vec.append(val)

        all_vec = tf.concat(vec, axis=0)
        square_term = tf.math.square(all_vec)
        sum_square = tf.reduce_sum(square_term)
        proximal_loss = 0.5 * mu * sum_square

        return proximal_loss