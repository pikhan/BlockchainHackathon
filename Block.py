import hashlib
import datetime
from Pyro5.api import expose, behavior, Daemon
import encryption as enc
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, VariableListProperty, ListProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Color, Rectangle


# force size of window here for kivy
Config.set('graphics', 'width', '1380')
Config.set('graphics', 'height', '900')


choice = -1


# class for containing our data to put inside the block
# dd --> due diligence
class HackathonData:
    def __init__(self, dd_type, dd_doc, dd_date, orig_fi_id, vendor_id, req_fi_id):
        self.dd_type = dd_type
        self.dd_doc = dd_doc  # should be .pdf or some kind of file like that
        self.dd_date = dd_date
        self.orig_fi_id = orig_fi_id
        self.vendor_id = vendor_id
        self.req_fi_id = req_fi_id

    def print_all_data(self):
        print("Type of Due Diligence:", self.dd_type)
        print("Document:", self.dd_doc)
        print("Date Completed:", self.dd_date)
        print("Original FI:", self.orig_fi_id)
        print("3rd Party Vendor:", self.vendor_id)
        print("Requesting FI:", self.req_fi_id)


# class for our actual Block
class HackathonBlock:
    def __init__(self, index, timestamp, data, prev_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hashing()

    def hashing(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.prev_hash).encode('utf-8'))
        return key.hexdigest()

    def get_index(self):
        return self.index

    def get_timestamp(self):
        return self.timestamp

    def get_data(self):
        return self.data

    def get_prev_hash(self):
        return self.prev_hash

    def get_hash(self):
        return self.hash

    def print_data(self):
        self.data.print_all_data()


# class for our Chain
@expose
@behavior(instance_mode="single")
class HackathonChain:
    def __init__(self):  # initializes the block chain with a Genesis block
        self.blocks = [self.get_genesis_block()]

    def get_genesis_block(self):
        return HackathonBlock(0,
                              datetime.datetime.utcnow(),
                              'Genesis',
                              'arbitrary')

    def add_block(self, dd_type, dd_doc, dd_date, orig_fi_id, vendor_id, req_fi_id):
        self.blocks.append(HackathonBlock(len(self.blocks),
                                          datetime.datetime.utcnow(),
                                          HackathonData(dd_type, dd_doc, dd_date, orig_fi_id, vendor_id, req_fi_id),
                                          self.blocks[len(self.blocks) - 1].hash))

    def get_chain_size(self):  # exclude genesis block
        return len(self.blocks) - 1

    def get_block_data(self, index):
        return self.blocks[index].get_data()

    def print_block_data(self, index):
        self.blocks[index].print_data()


# GUI class
class GUI(App):
    def build(self):
        layout = MyGui()
        Clock.schedule_interval(layout.update, 1.0 / 30.0)
        return layout


class MyGui(GridLayout):
    def __init__(self, **kwargs):
        super(MyGui, self).__init__(**kwargs)
        self.cols = 2
        self.old = 0

        self.blockLabel = Label(text=" BLOCKCHAIN SHIET", font_size=70)
        self.add_widget(self.blockLabel)
        right = ChoicesGui()
        self.add_widget(right)

    def update(self, dt):
        global choice
        self.updateRight(choice)

    def updateRight(self, choice):
        if self.old != choice:
            self.old = choice
            if self.old == 1:
                self.clear_widgets()
                self.add_widget(self.blockLabel)
                self.add_widget(TradeBlockGui())
            elif self.old == 2:
                print("Update GUI here")


class ChoicesGui(GridLayout):
    def __init__(self, **kwargs):
        super(ChoicesGui, self).__init__(**kwargs)
        self.rows = 2

        self.req = Button(text="Create new block", size_hint=[1, .5])
        self.add_widget(self.req)
        self.req.bind(on_press=self.reqPressed)

        self.up = Button(text="Upload", size_hint=[1, .5])
        self.add_widget(self.up)
        self.up.bind(on_press=self.upPressed)

    def reqPressed(self, btn):
        btnPres(1)

    def upPressed(self, btn):
        btnPres(2)


def btnPres(val):
    global choice
    choice = val

class TradeBlockGui(GridLayout):
    def __init__(self, **kwargs):
        super(TradeBlockGui, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 4

        self.add_widget(MyLabel(text="DD Type", font_size=45))
        self.dd_type = TextInput(multiline=False, font_size=35)
        self.add_widget(self.dd_type)

        self.add_widget(MyLabel2(text="Original ID", font_size=45))
        self.orig_id = TextInput(multiline=False, font_size=35)
        self.add_widget(self.orig_id)

        self.add_widget(MyLabel(text="Vendor ID", font_size=45))
        self.ven_id = TextInput(multiline=False, font_size=35)
        self.add_widget(self.ven_id)

        self.add_widget(MyLabel2(text="Request ID", font_size=45))
        self.req_id = TextInput(multiline=False, font_size=35)
        self.add_widget(self.req_id)


class MyLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, .82, .863, 0.9)
            Rectangle(pos=self.pos, size=self.size)


class MyLabel2(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, .82, .953, 0.9)
            Rectangle(pos=self.pos, size=self.size)




def main():
    print("@ top")
    chain = HackathonChain()
    key_chain = enc.HackathonKeyChain()
    chain.add_block('SSAE18 Soc2', 'audit.pdf', '10/27/2018', 'Equifax', 'Amazon', 'FICO')
    chain.print_block_data(1)
    print("@ exit")
    GUI().run()
    #Daemon.serveSimple(
            #{
            #    HackathonChain: "genesis.hackathonchain"
            #},
            #ns=False)


if __name__ == "__main__":
    main()
