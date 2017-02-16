import appdaemon.appapi as appapi
from utils import *
             
class doors(appapi.AppDaemon):

  def initialize(self):
    # self.LOGLEVEL="DEBUG"
    self.log("doors App")
    self.state={"22":"closed","23":"open"}
    self.door_list={"sensor.ge_32563_hinge_pin_smart_door_sensor_access_control_3_9":"group.office_lights"}
    for door in self.door_list:
      self.log("Activating listener for {}".format(door))
      self.listen_state(self.door_activity,door)

  def door_activity(self,entity_id,attributes,old,new,kwargs):
    self.log("enitty {} {}".format(entity_id,self.state[new]))
    elist=[]
    action_list={}
    entityin=None
    if entity_id in self.door_list:
      #action_list=self.build_light_list(self.door_list[entity_id])
      action_list["entity_id"]=self.door_list[entity_id]
      self.log("action_list={}".format(action_list))
      for e in action_list:
        self.log("e={}".format(e))
        if self.state[new]=="open":
          self.log("Turning on {}".format(action_list["entity_id"]))
          self.turn_on(action_list["entity_id"])
        else:
          self.log("Turning off {}".format(action_list["entity_id"]))
          self.turn_off(action_list["entity_id"])
    else:
      self.log("{} not found in {}".format(entity_id,self.door_list))

  def build_light_list(self,entityin):
    elist=[]
    for object in self.get_state(entityin,attribute='all')["attributes"]["entity_id"]:
      device, entity = self.split_entity(object)
      if device=="group":
        # if the device is a group recurse back into this function to process the group.
        elist.update(self.build_light_list(object))
      else:
        elist.append({"entity_id":object, "device":device,"entity":entity})
    self.log("elist={}".format(elist),level="INFO")
    return(elist)

  def log(self,msg,level="INFO"):
    obj,fname, line, func, context, index=inspect.getouterframes(inspect.currentframe())[1]
    super(doors,self).log("{} - ({}) {}".format(func,str(line),msg),level)

def set_house_state(self,entity,state):
    if self.entity_exists(entity):
      self.select_option(entity,state)
      retval=self.get_state(entity)
    else:
      retval=None
    return(retval)

def get_house_state(self,entity):
    if self.entity_exists(entity):
      state=self.get_state(entity)
      self.log("house state={}".format(state),"DEBUG")
    else:
      state=None
    return(state)


