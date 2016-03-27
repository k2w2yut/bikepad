class Player:
    MALE = 0
    FEMALE = 1
    
    weightHandicap = {
        # age   : weight
        "20-30" : 1,
        "31-35" : 1.05,
        "36-40" : 1.1,
        "41-45" : 1.15,
        "46-50" : 1.20,
        "51-55" : 1.25,
        "56-60" : 1.30,
        "61-65" : 1.35,
        "65-80" : 1.5
    }
    
    sexWeightHandicap = {
        "MALE" : 1,
        "FEMALE" : 1.1
    }
    
    # attributes
    sex = MALE
    age = None
    heartRate = None
    speed = None
             
    # weight
    hadicap_weight = None
    sex_handicap_weight = None
    
    
    def __init__(self, sex, age):
        # set sex handicap
        self.sex = sex
        self.age = age
        if self.sex == Player.MALE:
            self.sex_handicap_weight = self.sexWeightHandicap["MALE"]
        else:
            self.sex_handicap_weight = self.sexWeightHandicap["FEMALE"]

        # set general weight handicap            
        if self.age in xrange(20, 30):
            self.hadicap_weight = self.weightHandicap["20-30"]
        elif self.age in xrange(31, 35):
            self.hadicap_weight = self.weightHandicap["31-35"]
        elif self.age in xrange(36, 40):
            self.hadicap_weight = self.weightHandicap["36-40"]
        elif self.age in xrange(41, 45): 
            self.hadicap_weight = self.weightHandicap["41-45"]
        elif self.age in xrange(46, 50):
            self.hadicap_weight = self.weightHandicap["46-50"]
        elif self.age in xrange(51, 55):
            self.hadicap_weight = self.weightHandicap["51-55"]
        elif self.age in xrange(56, 60):
            self.hadicap_weight = self.weightHandicap["56-60"]
        elif self.age in xrange(61, 65):
            self.hadicap_weight = self.weightHandicap["61-65"]
        else:
            self.hadicap_weight = self.weightHandicap["65-80"]
            
    def get_speed(self):
        return self.speed * self.hadicap_weight * self.sex_handicap_weight
            
    def set_sex_age(self,sex,age):
        self.sex = sex
        self.age = age                      
            
          
