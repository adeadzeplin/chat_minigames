import socketio
import time
import multiprocessing
sio = socketio.Client()
chat_data_queue = None


@sio.event
def connect():
    print("I'm connected!")
    sio.emit('req')


@sio.on('chat_data')
def on_message(dat):
    global chat_data_queue
    if dat != 'None':
        # print(f'Data Received: {dat}')
        chat_data_queue['queueue'].put(dat)
    # try:
    #     req = chat_data_queue['request_export'].get(0)

    # except:
    #     req = None
    #     pass
    # if req != None:
    #
    #     print(req)
    sio.emit('req')

@sio.event
def connect_error(sid):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


def run_client_socket(q,ip='http://192.168.1.31:3333'):
    global chat_data_queue
    chat_data_queue = q
    sio.connect(ip)


if __name__ == '__main__':

    queue_dict = {
        'queueue': multiprocessing.Queue(),
        'request_import': multiprocessing.Queue(),
        'request_export': multiprocessing.Queue()
    }

    client_socket_process = multiprocessing.Process(target=run_client_socket, args=(queue_dict,))
    client_socket_process.start()
    client_socket_process.join()
