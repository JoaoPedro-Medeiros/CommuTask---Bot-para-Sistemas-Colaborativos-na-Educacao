class OnReadyEvent:
    def execute(self, username):
        print(f'Bot {username} está online!')

on_ready_var  = OnReadyEvent()