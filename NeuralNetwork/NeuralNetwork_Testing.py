import ast
import numpy
import random
import math
import copy



def SepDataAns(dans):
    global DataSet, Answers
    retData = []
    retAns = []
    for i in dans:
        retData.append(i[0])
        retAns.append(i[1])
    DataSet = retData
    Answers = retAns
    

def SortFunc(e):
    return(e[0])

def TrainNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss,TrainingLength):
    results = [TestNetwork(N,0,0,1,Data,Anss)]
    print("---INITIAL NETWORK SUCCESS---")
    print("")
    print(results[0][0])
    print("")
    print("------TRAINING------")
    print("")

    for i in range(TrainingLength):
        new = TestNetwork(results[0][1],BiasRange, WeightRange, Iterations,Data,Anss)
        results.append(new)
        results.sort(key=SortFunc)
        if i%5 == 0:
            print(str(i)+"/"+str(TrainingLength))
            
    print("")
    print("------TRAINING COMPLETE------")
    print("")
    print("--SUCCESS--")
    print(results[0][0])
    print("")
    
    return(results[0])

def TestSingleData(N,data,Answer):
    print("--Trying--")
    for Input in range(len(N[0])):
        N[0][Input].contents = data[Input]
    CalcNetwork(N)
    print("This should be close to " + str(Answer))
#    for out in range(len(N[-1])):
#        if out == Answer:
#            print("This should be a 1")
#        else:
#            print("This should be a 0")
#        print(N[-1][out].contents)
    for i in N[-1]:
        print(i.contents)
    print("---------------")

    
def ModifyNetwork(N, BiasRange, WeightRange):
    output = copy.deepcopy(N)
    for neurons in range(2,len(output),2):
        for neuron in range(len(output[neurons])):
            output[neurons][neuron].bias += random.uniform(-BiasRange,BiasRange)
    for connections in range(1,len(output),2):
        for connection in range(len(output[connections])):
            output[connections][connection].weight += random.uniform(-WeightRange,WeightRange)
    return(output)
def SuccessOfNetwork(N,Data,Anss):
    success = 0
    for Inputs in range(len(Data)):
        for Input in range(len(N[0])):
            N[0][Input].contents = Data[Inputs][Input]
        CalcNetwork(N)
        outputs = []
        for output in range(len(N[-1])):
            outputs.append(N[-1][output].contents)
        success += math.dist(outputs,Anss[Inputs])
     #       if output == Anss[Inputs]:
     #           print(N[-1][Anss[Inputs]].contents)
     #           success += math.dist([N[-1][Anss[Inputs]].contents],[1])
     #       else:
     #           success += math.dist([N[-1][Anss[Inputs]].contents],[0])
            
#        success += math.dist([N[-1][ID].contents],[Anss[Inputs]])


    return(success/len(Data))
   
######################################PROBLEM##########################
def TestNetwork(N,BiasRange, WeightRange, Iterations,Data,Anss):
    results = [[SuccessOfNetwork(N,Data,Anss),N]]
    for i in range(Iterations):
        testN = copy.deepcopy(N)
        testN = ModifyNetwork(testN, BiasRange, WeightRange)
        results.append([SuccessOfNetwork(testN,Data,Anss),testN])
    results.sort(key=SortFunc)
    if Iterations == 1:
        print("")
        print("----SUCCESS----")
        print(results[0][0])
        print("---------------")
    return(results[0])
    
def CreateNetwork(Type, inputs, layers, NeuronsPerLayer, outputs, load):
    if Type == "NewBasic":
        NewN = []
        for layer in range(0,layers):
            NewN.append([])
            for i in range(NeuronsPerLayer):
                neuron = Neuron(layer+1,i,0,0)
                NewN[layer].append(neuron)
        NewN.insert(0,[])
        NewN.append([])
        for i in range(inputs):
            neuron = Neuron(0,i,0,0)
            NewN[0].append(neuron)
        for i in range(outputs):
            neuron = Neuron(len(NewN)-1,i,0,0)
            NewN[-1].append(neuron)
        ConnectedNN = NewN
        for i in range(len(NewN)-1):
            ConnectedNN = CreateConnections(ConnectedNN, i*2, i*2+1, 0)
        return(ConnectedNN)
    elif Type == "Load":
        NewN = []

        for layer in range(len(load)):


            if layer%2 != 0:
                connections = []


                for i in range(len(load[layer])):
                    c = Connection(layer, i, load[layer][i])
                    connections.append(c)
                NewN.insert(layer,connections)

            else:
                neurons = []
                for i in range(len(load[layer])):
                    n = Neuron(layer, i, load[layer][i], 0)
                    neurons.append(n)
                NewN.insert(layer,neurons)
        
        return(NewN)
def CreateConnections(N, layer1, layer2, weights):
    cons = []
    Return = copy.deepcopy(N)
    if weights != 0:
        for i in range(len(N[layer1])*len(N[layer2])):
            c = Connection(layer2, i, weights[i])
            cons.append(c)
    else:
        for i in range(len(N[layer1])*len(N[layer2])):
            c = Connection(layer2, i, 0)
            cons.append(c)
    Return.insert(layer2, cons)
    for i in Return[layer2+1]:
        i.x = layer2+1
    return(Return)
def CalcNetwork(N):
    for i in range(2,len(N),2):
        for neuron in N[i]:
            neuron.CalcOutput(N)
            
def DrawNetwork(N):
    for layer in range(len(N)):
        
        if layer%2 != 0:
            connections = []
            for connection in range(len(N[layer])):
                connections.append(N[layer][connection].weight)
            print(connections)
        else:
            neurons = []
            for neuron in range(len(N[layer])):
                neurons.append(N[layer][neuron].bias)
            print(neurons)
def SaveNetwork(N):
    print("")
    output = []
    for layer in range(len(N)):
        if layer%2 != 0:
            connections = []
            for connection in range(len(N[layer])):
                connections.append(N[layer][connection].weight)
            output.append(connections)
        else:
            neurons = []
            for neuron in range(len(N[layer])):
                neurons.append(N[layer][neuron].bias)
            output.append(neurons)
    print("---------SAVE---------")
    print(output)
    print("-----------------------------------------------------")
class Connection:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight
class Neuron:
    def __init__(self, x, y, bias, contents):
        self.x = x
        self.y = y
        self.bias = bias
        self.contents = contents
    def CalcOutput(self,N):
        self.contents = 0
        counter = 0
        for i in N[self.x-2]:
            self.contents += i.contents * N[self.x-1][self.y*len(N[self.x-2])+counter].weight
            counter+=1

        self.contents += self.bias
        #Sigmoid function, S(x) = 1/(1+e^-x)
        self.contents = 1/(1+numpy.exp(-self.contents))

#==================================================================================================================#
#-------------------------------------------------CONFIGURATIONS---------------------------------------------------#
#==================================================================================================================#
        
#NN = CreateNetwork("NewBasic",2,2,3,2,0)
#NN = CreateNetwork("Load",2,2,3,2,[[0, 0], [2.0543093035668014, 2.4741533138948926, 0.74837439199015, 0.7710422145200428, -0.16703234743542472, -1.3948079686367958], [0.6963457602649132, 0.12553388527032006, -2.3694761038700958], [2.435440616272797, 1.9188554333461445, -3.8291532540356243, 0.7361508322464702, -1.9752097672697253, -0.790850062550275, 1.0492845380613898, -1.6630668250032283, 4.492803920554506], [3.4401376310528105, 4.4674703470040855, 5.029476163010856], [10.154406963319992, 8.44502664914806, 6.935567874707492, 7.670671405224791, 10.81935284108959, 8.560818708283632], [11.695111826774442, 10.808641135677922]])

#TestSingleData(NN,[0,0],0)

#NN = copy.deepcopy(TrainNetwork(NN,0.5,0.5,20,DataSet,Answers,20)[1])

#SaveNetwork(NN)

#==================================================================================================================#
#-------------------------------------------------USER-INTERFACE---------------------------------------------------#
#==================================================================================================================#


def Commands():
    print("")
    print("-----COMMANDS-----")
    print("")
    print("Create")
    print("Load")
    print("Train")
    print("Save")
    print("Draw")
    print("Test")
    print("ManualTest")
    print("SetData")
    print("SetAnswers")
    print("GetData")
    print("GetAnswers")
    print("Database")
    print("Run")
    print("SetOutputNames")
    print("Exit")
    
def Create():
    global NetworkActive, NN
    print("")
    print("-----CREATING-NEURAL-NETWORK-----")
    print("")
    print("amount of input neurons?")
    inputs = int(input())
    print("amount of neuron layers?")
    layers = int(input())
    print("amount of neurons per layer?")
    npl = int(input())
    print("amount of output neurons?")
    outputs = int(input())
    NN = CreateNetwork("NewBasic",inputs,layers,npl,outputs,0)
    print("NEURAL NETWORK CREATED SUCCESSFULLY----")
    NetworkActive = True
    
def Load():
    global NetworkActive, NN, f
    print("")
    print("-----LOADING-NEURAL-NETWORK-----")
    print("")
    print("Paste here your Neural Network")
    ans = input()
    if ans != "0":
        load = ast.literal_eval(ans)
        NN = CreateNetwork("Load",0,0,0,0,load)
        print("NEURAL NETWORK LOADED SUCCESSFULLY----")
        NetworkActive = True
    else:
        f = open(r"C:\Users\Francisco\Desktop\Coding\Python\NeuralNetwork\SquaresTrianglesNN_0.5.txt", "r")
        print("loaded")
        load = ast.literal_eval(f.read())
        NN = CreateNetwork("Load",0,0,0,0,load)
        print("NEURAL NETWORK LOADED SUCCESSFULLY----")
        NetworkActive = True
        f.close()

def Train():
    global weightChange, biasChange, iterations, configurated, NN, DataSet, Answers
    print("")
    if configurated == False:
        print("How much should the weights vary?")
        weightChange = float(input())
        print("How much should the biases vary?")
        biasChange = float(input())
        print("How many different settings should be tested per iteration?")
        iterations = int(input())
        configurated = True 
    else:
        print("Do you want to change your configurations?(write yes or no)")
        yess = input()
        if yess == "yes":
            print("How much should the weights vary?")
            weightChange = float(input())
            print("How much should the biases vary?")
            biasChange = float(input())
            print("How many different settings should be tested per iteration?")
            iterations = int(input())
    print("How many iterations should the training last?")
    its = int(input())
    NN = copy.deepcopy(TrainNetwork(NN,weightChange,biasChange,iterations,DataSet,Answers,its)[1])
def ManualTest():
    print("")
    print("Write the data you want to input")
    data = ast.literal_eval(input())
    print("What should be the outputs?")
    outn = ast.literal_eval(input())
    TestSingleData(NN,data,outn)
def Test():
    global DataSet, Answers
    print("")
    TestNetwork(NN,0,0,1,DataSet,Answers)
def SON():
    print("")
    print("Write the output names in order")
    global OutputNames
    OutputNames = ast.literal_eval(input())
def Run():
    if OutputNames != [0]:
        print("")
        print("Write the input")
        data = ast.literal_eval(input())
        print("--Testing--")
    for Input in range(len(NN[0])):
        NN[0][Input].contents = data[Input]
    CalcNetwork(NN)
    outputs = []
    for i in range(len(NN[-1])):
        outputs.append((NN[-1][i].contents,i))
    outputs.sort()
    print(OutputNames[outputs[-1][1]])
    print("---------------")

            
print("=================================================================================================")
print("-----------------------------------------NEURAL-NETWORK------------------------------------------")
print("=================================================================================================")
print("")

        
DataSet = [[0,0],[0,1],[1,0],[1,1]]
Answers = [[0,1],[1,0],[1,0],[0,1]]
OutputNames = [0]

running = True

NetworkActive = False
configurated = False
weightChange = 0
biasChange = 0
iterations = 0


while running:
    try:
        print("")
        print("Type COMMANDS for a list of all commands available, Type HELP <command name> for details on what a command does")
        print("")
        command = input()
        if command == "COMMANDS":
            Commands()
        elif command == "Create":
            Create()
        elif command == "Load":
            Load()
        elif command == "SetData":
            DataSet = ast.literal_eval(input())
        elif command == "SetAnswers":
            Answers = ast.literal_eval(input())
        elif command == "GetData":
            print(DataSet)
        elif command == "GetAnswers":
            print(Answers)
        elif command == "Exit":
            running = False
        elif command == "SetOutputNames" or command == "SON":
            SON()
        elif command == "Database":
            print("")
            print("paste your database")
            datab = ast.literal_eval(input())
            SepDataAns(datab)
        elif NetworkActive:
            if command == "Train":
                Train()
            elif command == "Save":
                SaveNetwork(NN)
            elif command == "ManualTest":
                ManualTest()
            elif command == "Test":
                Test()
            elif command == "Draw":
                DrawNetwork(NN)
            elif command == "Run":
                Run()
    except:
        print("ERROR")

#XOR gate
#[[0, 0], [1.4204311002447603, -5.309028174705563, 3.3092154925604227, 2.8825343381492154, -7.873405532491077, -6.019416861180404, 5.125575034962067, -2.8666983888411828], [1.614435601644602, 0.016131555595663205, 1.73897967586091, 1.2359648104132177], [-8.974088717467243, -4.60058001291934, 7.353011153904542, 9.17388268584272, 3.829650109522766, 0.37428868908721535, -3.5579007410461774, -4.306165596088678, -0.9357880904781496, 4.603061457161539, 0.5723375466781854, 3.0543949617987685, 4.5548775339863035, 1.3716862681729667, -5.429803610457084, -5.078576612706518], [-0.7849711262945884, -0.5714722475247994, -0.930940443740087, 0.23697863009830927], [-6.081119873037392, -1.696696021860504, -0.48851929757589674, 6.20987846893892, -8.8760245154546, 0.41450976092407577, 0.47620834872248385, 0.7480093432555303, 6.801552592059402, 1.2410306934441886, -2.593870522464482, -6.982363501554641, -8.684307901569992, -4.439388595453959, 1.9151387563026683, 5.984997529476109], [0.4152379118970686, 1.829816690195707, 1.0920906099376395, -0.15734449096419909], [4.634434189910534, 5.990777986795788, -14.415159310672493, 8.49614710674933, -8.33059698918259, -4.623930893435514, 14.0771155844683, -8.638855053379118], [-1.7272987121634253, 2.978394590069382]]
#["One","Zero"]

#Lines and dotted lines
#[[0, 0, 0, 0, 0, 0, 0, 0], [-3.076322834376393, 1.0461766439931646, -3.814726632672155, 1.8679138480387603, -6.112019773088691, -0.9873710517320012, -0.00027598901194891834, 3.3157951489207367, -1.1694079693177781, 3.9906420555377315, -1.481603389512284, 0.14503979403048828, -0.5983057794030807, 2.059730240833108, -0.016363714806785445, 3.4911422528230136, 1.0443391932370916, -3.0697340673808964, 3.3114705127328548, -5.3554198870343495, 0.023920555012774014, -7.2503908379172985, 4.722995179488404, -0.90989246341175, -1.9610422412503956, 0.9696669211548621, -0.4949501817284151, -0.2689250274489119, -1.5855165408823804, -0.3417782320782806, -0.07524596553216312, -3.545265607246285, -4.057124519947687, -1.4469129810395347, -4.171291994035639, -0.41829610544733764, -3.084029174919286, -7.430095427630182, 0.7312976268290542, 7.336322847067308, -4.104219861194783, -15.330833918561858, -0.32260206163313154, 0.1484798113368958, -7.308403336180219, 0.09893109039565084, -4.172922707414892, 2.4632437212731335, -1.7412008231396796, -1.304969789902096, 5.0988600426664545, -3.5964079274775127, 4.420679907210927, -5.138893791474014, -6.976641083227061, 2.141560049264158, 4.023876740536756, 4.346614762753318, -0.36920636055712897, 3.3652552366626267, 1.5615046059518334, -3.8548575410432937, 0.12412810393113083, -3.666927388805608, 3.679925364961746, 1.2025368602285003, -5.875389792758521, 0.40210416633451307, -0.76081962397935, -1.7718073902209284, -0.0864683216573846, 3.484010864097403, -2.6575518191344436, 0.49702205427520607, -0.5281665197834212, -0.8226536143976058, 2.4660046250577476, -2.1516249421549, -6.973130801934341, -0.7302965793060023], [-0.7495433698693911, 0.15947895072837465, -1.8458650883369134, -0.5451004399449518, 1.2379678555719689, 0.8478617257657506, -1.86983093761013, -1.6526897981351647, -1.9016870587831531, 0.40420494760379644], [4.916703464372742, -4.718790350958589, 3.54877302211695, -3.822841452482854, -0.566476551067107, -6.738557236558112, 1.111790589797051, -0.07656841271448489, 3.043696656900494, 6.619048700977959, -3.8213426091825897, 2.5922780622634765, -3.1503214348362145, 1.6167240761157848, -4.5361742648419, -0.02155562702763869, 3.1872772200643853, 3.3693437803696233, -3.297678165225877, -0.06223203315631298, -0.4439324112765455, 6.241702647810071, 1.7362338596832174, -8.674164339477585, -1.0303794772557247, -0.24864114119730996, -4.949596184715819, 5.001552209763968, 3.1174136960274557, -0.6828339322394006, -0.7859138779337391, -0.8377888276392053, 4.7129638407570935, -6.344981231823519, -3.6159475982750195, 4.756719813869317, 0.8271682739238956, -0.13333953846779678, -2.9490902307654183, 0.2237966579502576, -3.449314862572717, 1.3118050098702505, -0.22434843897999612, -3.8444055108067365, 0.31215600841586155, -5.454939359510219, 3.331299842298794, 1.1158284634006923, -0.8730649187227472, 1.3582522199824525, 2.727981492037973, -2.332268174819456, 2.6018133303788455, 1.793546964667013, -1.4302076757836282, -0.29271478190543265, -2.75063634264489, -4.385946928076994, -0.7700988235861306, -1.9064636523668212, -3.69198031834352, -0.7330191456541897, -2.7461954851595864, -1.7725347879183322, 2.1241440395911755, -0.5389225948091306, -0.9858726427960219, 3.9991190511948798, -2.8123604537892297, 7.242095963181035, -1.5260293548171147, -1.6068569140018103, 1.7588991358808097, 3.484644686629565, -4.398836451273768, 1.402600612869215, -3.880955010738763, -4.608124702287514, 0.10973445647423641, -0.4944217400193369, 4.708498434058562, -6.299837129489461, 1.587796708843576, -2.124594527359056, 3.4982609206257993, 3.9288520320910147, 2.282477570262055, -7.094835195078229, 0.21701847160190324, 1.1190300558436443, -6.749256161275619, 2.4920332830545213, 1.0636785268420974, -2.8154557183180833, -0.20525966903294834, -3.6383920008212782, -7.017977531125777, -2.4630985102973133, 1.9222328990988786, -2.5259510965294036], [-1.223164730000956, 1.9991706775025482, 0.7190097897491335, -0.6853856377771409, 0.17679392434055816, -0.6936476806322942, -1.4845509695689385, -0.0011903487815950603, -0.8807402089617871, 0.3781089014023957], [4.036246190212149, 2.491970813617473, -2.044295530585388, 5.036090916703066, -3.9705735115948997, 3.522771548347006, 0.5153278773952661, -1.3591470883349452, 1.6102717468512677, -3.1745775087923733, 2.914440485378897, 2.068193431204991, -6.3435289336429515, 0.128030866373664, -0.4691699262473411, 2.699102336830485, 1.2987324030940024, -1.0728857672916385, 5.489169263261104, -4.037049986242959, 7.791906255135151, 1.9475771035722493, 1.6211155232945291, 0.4660740986094739, -4.988274481832065, -0.4564661513421333, 0.07783085652057575, -0.5657773091396167, 3.9364925040245495, -4.7029609567151445, -3.0672428198733486, 0.8258896620953704, -1.2177841170499355, -0.5831706913996465, 3.931324554571986, 2.3238939290320735, 0.40202942367371586, -1.5034445361660143, 5.3307800461001, -1.518143742530019, -4.215467001528985, 6.2390282584323815, 1.8381859371505147, 3.715058527066506, -2.790960970039743, 4.466707392351701, 0.9953188052562845, 1.3106673314814696, -1.5402546700193567, 3.2657431342194108, 3.2040757754985627, 4.75159640155839, 1.7980483731837342, 2.219108329304707, -0.002357599121768361, 3.874677286389107, -0.5497889127246015, 1.3457428455950664, -5.278929156141646, -1.1226028147233846, 0.12149726548492024, -1.6799539693100682, 4.968224312565125, -1.3462425900857475, 3.3437864684937404, -3.9815102885997096, 2.88150388441602, -4.616265824964808, -2.149781934115876, 0.8721757693166349, -1.139199229368318, 5.743938656347556, -6.686786344817967, -4.630562876747363, 3.7030396617094277, -0.07080112372536385, -1.1142212092875154, -5.2705880119368755, -0.44164794492417525, -2.7648243328908775, -6.671921138124444, 6.622166554866718, -3.9847103687080074, -3.202153279345133, 2.9285065080334736, -2.3211732914323155, -2.5800250866724936, -2.1572979272704114, -6.02405339631194, 3.390098520496453, 2.8282335532929275, -0.628887409007983, 2.897619676534099, 5.460346109610415, -2.8740136909260654, -1.364371755756813, 3.098084431542744, 1.0744135696649058, -2.8341529345807626, 5.716940473507638], [0.9985475580915564, 2.4329736516371865, -0.7135390792322212, 0.5394993516191908, 0.6591257968718705, 1.6368007968950644, -3.1251157107081786, -0.4612221455959629, 0.552254478632231, -0.2929189240480269], [-3.3729672111404065, -3.6654035626248196, -5.0598812052727595, 1.6940539441904336, -1.394856693183588, 4.071493011007691, -4.650573581428331, 0.668106124840496, 1.9333277834644118, 1.775948626276298, 5.084906850486341, 1.3377559593999395, -4.1262954950192245, -4.761761729919591, -3.1236027610585646, -3.43188172400046, -6.240180613387857, 2.7289614812972833, -1.9917801768149506, -3.2522065740425252, -0.30040250687713344, -1.5545465132326945, 0.5064437385628034, -2.1690827788171156, 0.7137078995373497, 0.2931388540316131, -3.423168940502677, 1.4146214116121074, -4.726186134769079, 5.0778033774354565, -7.8015145424690795, -4.410200828568802, -7.2798626897845775, 2.040955765523827, -1.0653791827835901, 0.5112416117829962, 1.9983423787383339, 3.70376303611816, 0.1228798539147975, 1.3625755692188193, -0.45250137364275944, -2.627050843334334, 1.6052778577853595, 1.223566827585581, -1.6891945503618704, 2.843372175851484, -4.195241806957806, 4.807496665212685, -4.895839125863576, 3.349042008557161, 4.444669317052169, 2.502104319846362, -2.1862498657555083, -1.4180254757079143, 0.6444036868195734, 0.8908583225418606, 1.322521573846332, -3.2157057521679295, -9.041371659833782, 0.8211069735486508, -3.1856636384254093, 2.8637509915980157, -2.037154995257994, -2.331242683692878, -0.30997224194899864, -0.6749282756757442, 1.2818641591811593, -1.2537882798647888, 1.2158755631059592, 4.410528448090496, 2.866905909690194, 1.3660709657840187, 5.812238913241987, -4.032145730401861, 3.785938251119286, -3.7190812587881346, 0.7889463161308007, -0.3441551480735868, -1.3531934204540697, -0.6363402001884527, -0.12982117467665577, 2.901984061177934, -5.22329228784832, -1.142722081882998, 0.6081725671844158, 4.418952164380141, -7.771940802624028, 4.028677795427889, 5.972425657469049, 1.4180189699266084, -0.8039973353185477, 1.018102078638277, -4.503372502793586, 4.860877566955015, -2.8162914495604987, -0.2665590996718722, -6.126401591082502, 5.767638489563972, 4.657989168506641, -0.22580483710151034], [1.2504167549163674, 1.3556207287033597, 2.0288562619583645, -1.5427022254787437, 1.5573948159599804, 0.49406491166441907, -1.3990632131087721, -1.541486508466269, -0.988405878048479, 1.3659142733511929], [-4.1525205466358575, 3.361207475033111, 4.725690347497042, -7.788928506614039, 2.154892499030372, 6.890771664535579, -3.936651233653574, 10.96540603330955, -12.33388371035088, -3.3543816728459785, 0.5844328446802555, 1.4958624704214534, -0.238694394505222, 11.164521025251544, -4.238137390134864, -5.842934572835775, 1.0220941945368685, -13.647645115190818, 11.873959663079637, 8.503687804415124], [2.929133112044037, -2.6950849053721613]]
# [[1,1,1,1,1,1,1,1],[1,0,1,0,1,0,1,0],[1,1,1,1,0,0,0,0],[0,0,0,1,0,1,0,1],[0,0,0,1,1,1,0,0],[1,0,1,0,1,0,0,0],[0,0,0,0,1,1,1,1],[0,1,0,1,0,1,0,1]]
# [[0,1],[1,0],[0,1],[1,0],[0,1],[1,0],[0,1],[1,0]] Answers
# ["Dotted","Line"]