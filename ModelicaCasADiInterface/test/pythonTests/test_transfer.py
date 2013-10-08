from casadi import *

## In this file there are tests for transferModelica and transferOptimica. A subset of the transferOptimica
## tests are equal to the transferModelica tests. If a new test is added to the Modelica transfer this test
## should also be added to the Optimica transfer test.
##
## There are also tests for the correct transfer of the MX representation of expressions and various
## Modelica constructs from JModelica.org, testing the underlying infrastructure and the aspect in JModelica
## that provides the functionality. 


# Common variables used in the tests
x1 = MX("x1")
x2 = MX("x2")
der_x1 = MX("der_x1")
der_x2 = MX("der_x2") 
modelFile = "../common/atomicModelicaModels.mo"

# Is run before anything else
def setup_module(module):
    setUpJVM() 

# Is run after everything else
def teardown_module(module):
    tearDownJVM()
    
def assertNear(val1, val2, tol):
    assert abs(val1 - val2) < tol
    
##############################################
#                                            # 
#          MODELICA TRANSFER TESTS           #
#                                            #
##############################################
    
def test_ModelicaAliasVariables():
    model = transferModelicaModel("atomicModelAlias", modelFile)
    assert not model.getVariableByName("x").isNegated()
    assert model.getVariableByName("z").isNegated()
    assert str(model.getVariableByName("x")) == "MX(x), alias: y, declaredType : Real"
    assert str(model.getModelVariableByName("x")) == "MX(y), declaredType : Real"
    assert str(model.getVariableByName("y")) == "MX(y), declaredType : Real"
    assert str(model.getModelVariableByName("y")) == "MX(y), declaredType : Real"
    assert str(model.getVariableByName("z")) == "MX(z), alias: y, declaredType : Real"
    assert str(model.getModelVariableByName("z")) == "MX(y), declaredType : Real"
    

def test_ModelicaSimpleEquation():
    assert str(transferModelicaModel("AtomicModelSimpleEquation", modelFile).getDaeResidual()) == str(x1 - der_x1) 

def test_ModelicaSimpleInitialEquation():
    assert str(transferModelicaModel("AtomicModelSimpleInitialEquation", modelFile).getInitialResidual())  == str(MX(1)-x1)

def test_ModelicaFunctionCallEquations():
    assert( repr(transferModelicaModelWithoutInlining("AtomicModelFunctionCallEquation", modelFile).getDaeResidual()) == 
                ("MX(vertcat((x1-der_x1),(vertcat(function(\"AtomicModelFunctionCallEquation.f\")" + 
                ".call([x1]){0},function(\"AtomicModelFunctionCallEquation.f\").call([x1]){1})-vertcat(x2,x3))))") )  
                
def test_ModelicaBindingExpression():
    model =  transferModelicaModel("AtomicModelAttributeBindingExpression", modelFile)
    dependent =  model.getVariableByKind(Model.REAL_PARAMETER_DEPENDENT)
    independent =  model.getVariableByKind(Model.REAL_PARAMETER_INDEPENDENT)
    actual =  str(independent[0].getAttribute("bindingExpression")) + str(dependent[0].getAttribute("bindingExpression"))
    expected = str(MX(2)) + str(MX("p1"))
    assert actual == expected

def test_ModelicaUnit():
    model =  transferModelicaModel("AtomicModelAttributeUnit", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("unit")) == str(MX("kg")) 

def test_ModelicaQuantity():
    model =  transferModelicaModel("AtomicModelAttributeQuantity", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("quantity")) == str(MX("kg")) 

def test_ModelicaDisplayUnit():
    model =  transferModelicaModel("AtomicModelAttributeDisplayUnit", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("displayUnit")) == str(MX("kg")) 

def test_ModelicaMin():
    model =  transferModelicaModel("AtomicModelAttributeMin", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str((diffs[0].getAttribute("min"))) == str(MX(0)) 

def test_ModelicaMax():
    model =  transferModelicaModel("AtomicModelAttributeMax", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("max")) == str(MX(100))
    
def test_ModelicaStart():
    model =  transferModelicaModel("AtomicModelAttributeStart", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("start"))  == str(MX(0.0005))
    
def test_ModelicaFixed():
    model =  transferModelicaModel("AtomicModelAttributeFixed", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("fixed")) == str(MX(True))

def test_ModelicaNominal():
    model =  transferModelicaModel("AtomicModelAttributeNominal", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("nominal")) == str(MX(0.1))
        
def test_ModelicaComment():
    model =  transferModelicaModel("AtomicModelComment", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("comment")) == str(MX("I am x1's comment"))
        
def test_ModelicaRealDeclaredType():
    model =  transferModelicaModel("AtomicModelDerivedRealTypeVoltage", modelFile)
    assert str(model.getVariableTypeByName("Voltage")) == ("Type name: Voltage, base type: Real, attributes:" 
                                                           "\n\tquantity = MX(ElectricalPotential)\n\tunit = MX(V)")
   
def test_ModelicaDerivedTypeDefaultType():
    model =  transferModelicaModel("AtomicModelDerivedTypeAndDefaultType", modelFile)
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert int(diffs[0].getDeclaredType().this) == int(model.getVariableTypeByName("Voltage").this)
    assert int(diffs[1].getDeclaredType().this) == int(model.getVariableTypeByName("Real").this)
    
def test_ModelicaIntegerDeclaredType():
    model =  transferModelicaModel("AtomicModelDerivedIntegerTypeSteps", modelFile)
    print str(model.getVariableTypeByName("Steps"))
    assert str(model.getVariableTypeByName("Steps")) == ("Type name: Steps, base type: Integer, attributes:"
                                                                "\n\tquantity = MX(steps)")
    
def test_ModelicaBooleanDeclaredType():
    model =  transferModelicaModel("AtomicModelDerivedBooleanTypeIsDone", modelFile)
    print str(model.getVariableTypeByName("IsDone"))
    assert str(model.getVariableTypeByName("IsDone")) == ("Type name: IsDone, base type: Boolean, attributes:" 
                                                           "\n\tquantity = MX(Done)")

def test_ModelicaRealConstant():
    model =  transferModelicaModel("atomicModelRealConstant", modelFile)
    constVars =  model.getVariableByKind(Model.REAL_CONSTANT)
    assert str(constVars[0].getVar()) == str(MX("pi"))
    assertNear(constVars[0].getAttribute("bindingExpression").getValue(), 3.14, 0.0000001)

def test_ModelicaRealIndependentParameter():
    model =  transferModelicaModel("atomicModelRealIndependentParameter", modelFile)
    indepParam =  model.getVariableByKind(Model.REAL_PARAMETER_INDEPENDENT)
    assert str(indepParam[0].getVar()) == str(MX("pi"))
    assertNear(indepParam[0].getAttribute("bindingExpression").getValue(), 3.14, 0.0000001)
        
def test_ModelicaRealDependentParameter():
    model =  transferModelicaModel("atomicModelRealDependentParameter", modelFile)
    depParam =  model.getVariableByKind(Model.REAL_PARAMETER_DEPENDENT)
    indepParam =  model.getVariableByKind(Model.REAL_PARAMETER_INDEPENDENT)
    assert str(2*(indepParam[0].getVar())) == str(depParam[0].getAttribute("bindingExpression"))
    
def test_ModelicaDerivative():
    model =  transferModelicaModel("atomicModelRealDerivative", modelFile)
    assert str(model.getVariableByKind(Model.DERIVATIVE)[0].getVar()) == str(der_x1)
    
def test_ModelicaDifferentiated():
    model = transferModelicaModel("atomicModelRealDifferentiated", modelFile)
    diff = model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diff[0].getVar()) == str(x1)
        
def test_ModelicaRealInput():
    model =  transferModelicaModel("atomicModelRealInput", modelFile)
    ins =  model.getVariableByKind(Model.REAL_INPUT)
    assert str(ins[0].getVar()) == str(x1)

def test_ModelicaAlgebraic():
    model =  transferModelicaModel("atomicModelRealAlgebraic", modelFile)
    alg =  model.getVariableByKind(Model.REAL_ALGEBRAIC)
    assert str(alg[0].getVar()) == str(x1)
    
def test_ModelicaRealDisrete():
    model =  transferModelicaModel("atomicModelRealDiscrete", modelFile)
    realDisc =  model.getVariableByKind(Model.REAL_DISCRETE)
    assert str(realDisc[0].getVar()) == str(x1)
    
def test_ModelicaIntegerConstant():
    model =  transferModelicaModel("atomicModelIntegerConstant", modelFile)
    constVars =  model.getVariableByKind(Model.INTEGER_CONSTANT)
    assert str(constVars[0].getVar()) == str(MX("pi"))
    assertNear( constVars[0].getAttribute("bindingExpression").getValue(), 3, 0.0000001)
    
def test_ModelicaIntegerIndependentParameter():
    model =  transferModelicaModel("atomicModelIntegerIndependentParameter", modelFile)
    indepParam =  model.getVariableByKind(Model.INTEGER_PARAMETER_INDEPENDENT)
    assert str(indepParam[0].getVar()) == str(MX("pi"))
    assertNear( indepParam[0].getAttribute("bindingExpression").getValue(), 3, 0.0000001 )
    
def test_ModelicaIntegerDependentConstants():
    model =  transferModelicaModel("atomicModelIntegerDependentParameter", modelFile)    
    depParam =  model.getVariableByKind(Model.INTEGER_PARAMETER_DEPENDENT)
    indepParam =  model.getVariableByKind(Model.INTEGER_PARAMETER_INDEPENDENT)
    assert str(2*(indepParam[0].getVar())) == str(depParam[0].getAttribute("bindingExpression"))

def test_ModelicaIntegerDiscrete():
    model =  transferModelicaModel("atomicModelIntegerDiscrete", modelFile)
    intDisc =  model.getVariableByKind(Model.INTEGER_DISCRETE)
    assert str(intDisc[0].getVar()) == str(x1)
    
def test_ModelicaIntegerInput():
    model =  transferModelicaModel("atomicModelIntegerInput", modelFile)    
    intIns =  model.getVariableByKind(Model.INTEGER_INPUT)
    assert str(intIns[0].getVar()) == str(x1)
    
def test_ModelicaBooleanConstant():
    model =  transferModelicaModel("atomicModelBooleanConstant", modelFile)
    constVars =  model.getVariableByKind(Model.BOOLEAN_CONSTANT)
    assert str(constVars[0].getVar()) == str(MX("pi"))
    assertNear( constVars[0].getAttribute("bindingExpression").getValue(), MX(True).getValue(), 0.0000001 )
    
def test_ModelicaBooleanIndependentParameter():
    model =  transferModelicaModel("atomicModelBooleanIndependentParameter", modelFile)
    indepParam =  model.getVariableByKind(Model.BOOLEAN_PARAMETER_INDEPENDENT)
    assert str(indepParam[0].getVar()) == str(MX("pi"))
    assertNear( indepParam[0].getAttribute("bindingExpression").getValue(), MX(True).getValue(), 0.0000001 )
    
def test_ModelicaBooleanDependentParameter():
    model =  transferModelicaModel("atomicModelBooleanDependentParameter", modelFile)    
    depParam =  model.getVariableByKind(Model.BOOLEAN_PARAMETER_DEPENDENT)  
    indepParam =  model.getVariableByKind(Model.BOOLEAN_PARAMETER_INDEPENDENT)
    assert str( indepParam[0].getVar().logic_and(MX(True)) ) == str(depParam[0].getAttribute("bindingExpression"))
    
def test_ModelicaBooleanDiscrete():
    model =  transferModelicaModel("atomicModelBooleanDiscrete", modelFile)        
    boolDisc =  model.getVariableByKind(Model.BOOLEAN_DISCRETE)
    assert str(boolDisc[0].getVar()) == str(x1)

def test_ModelicaBooleanInput():
    model =  transferModelicaModel("atomicModelBooleanInput", modelFile)
    boolIns =  model.getVariableByKind(Model.BOOLEAN_INPUT)
    assert str(boolIns[0].getVar()) == str(x1)
        
def test_ModelicaModelFunction():
    model =  transferModelicaModel("simpleModelWithFunctions", "../common/modelicaModels.mo")
    expectedPrint = ("ModelFunction : function(\"simpleModelWithFunctions.f\")\n Inputs (2):\n"
                            "  0. 1-by-1 (dense)\n"
                            "  1. 1-by-1 (dense)\n"
                            " Outputs (2):\n"
                            "  0. 1-by-1 (dense)\n"
                            "  1. 1-by-1 (dense)\n"
                            "@0 = input[0]\n"
                            "@1 = input[1]\n"
                            "{@2,@3} = function(\"simpleModelWithFunctions.f2\").call([@0,@1])\n"
                            "output[0] = @2\n"
                            "output[1] = @3\n"
                            "ModelFunction : function(\"simpleModelWithFunctions.f2\")\n Inputs (2):\n"
                            "  0. 1-by-1 (dense)\n"
                            "  1. 1-by-1 (dense)\n"
                            " Outputs (2):\n"
                            "  0. 1-by-1 (dense)\n"
                            "  1. 1-by-1 (dense)\n" 
                            "@0 = Const<0.5>(scalar)\n"
                            "@1 = input[0]\n"
                            "@0 = (@0*@1)\n"
                            "output[0] = @0\n"
                            "@2 = input[1]\n"
                            "@0 = (@2+@0)\n"
                            "output[1] = @0\n")
    mf_1 = model.getModelFunctionByName("simpleModelWithFunctions.f")
    mf_2 = model.getModelFunctionByName("simpleModelWithFunctions.f2")
    actual = str(mf_1) + str(mf_2)
    assert expectedPrint == actual

def test_ModelicaDependentParametersCalculated():
    model =  transferModelicaModel("atomicModelDependentParameter", modelFile)
    model.calculateValuesForDependentParameters()
    depVars = model.getVariableByKind(Model.REAL_PARAMETER_DEPENDENT)
    assert depVars[0].getAttribute("evaluatedBindingExpression").getValue() == 20
    assert depVars[1].getAttribute("evaluatedBindingExpression").getValue() == 20
    assert depVars[2].getAttribute("evaluatedBindingExpression").getValue() == 200

def test_ModelicaFunctionCallEquationForParameterBinding():
    model =  transferModelicaModelWithoutInlining("atomicModelPolyOutFunctionCallForDependentParameter", modelFile)
    model.calculateValuesForDependentParameters()
    expected = ("MX(temp_1[1]), declaredType : Real, attributes:\n"
                "\tbindingExpression = MX(function(\"atomicModelPolyOutFunctionCallForDependentParameter.f\").call([p1]){0})\n"
                "\tevaluatedBindingExpression = MX(Const<2>(scalar))\n"
                "MX(temp_1[2]), declaredType : Real, attributes:\n"
                "\tbindingExpression = MX(function(\"atomicModelPolyOutFunctionCallForDependentParameter.f\").call([p1]){1})\n"
                "\tevaluatedBindingExpression = MX(Const<4>(scalar))\n"
                "MX(p2[1]), declaredType : Real, attributes:\n"
                "\tbindingExpression = MX(temp_1[1])\n"
                "\tevaluatedBindingExpression = MX(Const<2>(scalar))\n"
                "MX(p2[2]), declaredType : Real, attributes:\n"
                "\tbindingExpression = MX(temp_1[2])\n"
                "\tevaluatedBindingExpression = MX(Const<4>(scalar))\n")
    actual = ""
    for var in model.getVariableByKind(Model.REAL_PARAMETER_DEPENDENT):
        actual += str(var) + "\n"
    print expected, "\n", actual
    assert actual == expected

##############################################
#                                            # 
#          OPTIMICA TRANSFER TESTS           #
#                                            #
##############################################

optproblemsFile = "../common/atomicOptimizationProblems.mop"

def test_OptimicaAliasVariables():
    model = transferOptimizationProblem("atomicModelAlias", modelFile).getModel()
    assert not model.getVariableByName("x").isNegated()
    assert model.getVariableByName("z").isNegated()
    assert str(model.getVariableByName("x")) == "MX(x), alias: y, declaredType : Real"
    assert str(model.getModelVariableByName("x")) == "MX(y), declaredType : Real"
    assert str(model.getVariableByName("y")) == "MX(y), declaredType : Real"
    assert str(model.getModelVariableByName("y")) == "MX(y), declaredType : Real"
    assert str(model.getVariableByName("z")) == "MX(z), alias: y, declaredType : Real"
    assert str(model.getModelVariableByName("z")) == "MX(y), declaredType : Real"

def computeStringRepresentationForContainer(myContainer):
    stringRepr = ""
    for index in range(len(myContainer)):
        stringRepr += str(myContainer[index])
    print stringRepr
    return stringRepr

def test_OptimicaLessThanConstraint():
    optProblem =  transferOptimizationProblem("atomicOptimizationLEQ", optproblemsFile);
    expected = repr(x1) + " <= " + repr(MX(1.0))
    print expected
    
    assert( computeStringRepresentationForContainer(optProblem.getPathConstraints()) == expected)

def test_OptimicaGreaterThanConstraint():
    optProblem =  transferOptimizationProblem("atomicOptimizationGEQ", optproblemsFile)
    expected = repr(x1) + " >= " + repr(MX(1.0))
    assert( computeStringRepresentationForContainer(optProblem.getPathConstraints()) == expected)

def test_OptimicaStartTime():
    optProblem =  transferOptimizationProblem("atomicOptimizationStart5", optproblemsFile)
    assert( optProblem.getStartTime().getValue() == 5)
    
def test_OptimicaFinalTime():
    optProblem =  transferOptimizationProblem("atomicOptimizationFinal10", optproblemsFile)
    assert( optProblem.getFinalTime().getValue() == 10)

def test_OptimicaLagrangeTerm():
    optProblem =  transferOptimizationProblem("atomicLagrangeX1", optproblemsFile)
    assert str(optProblem.getLagrangeTerm()) == str(x1) 
    optProblem =  transferOptimizationProblem("atomicLagrangeNull", optproblemsFile)
    assert str(optProblem.getLagrangeTerm()) == str(MX(0))  

def test_OptimicaMayerTerm():
    optProblem =  transferOptimizationProblem("atomicMayerFinalTime", optproblemsFile)
    assert str(optProblem.getMayerTerm()) == str(MX("finalTime")) 
    optProblem =  transferOptimizationProblem("atomicMayerNull", optproblemsFile)
    assert str(optProblem.getMayerTerm()) == str(MX(0))

def test_OptimicaFree():
    model =  transferOptimizationProblem("atomicWithFree", optproblemsFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str((diffs[0].getAttribute("free"))) == str(MX(False))

def test_OptimicaInitialGuess():
    model =  transferOptimizationProblem("atomicWithInitialGuess", optproblemsFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("initialGuess")) == str(MX(5))

def test_OptimicaSimpleEquation():
    assert str(transferOptimizationProblem("AtomicModelSimpleEquation", modelFile).getModel().getDaeResidual()) == str(x1 - der_x1) 

def test_OptimicaSimpleInitialEquation():
    assert str(transferOptimizationProblem("AtomicModelSimpleInitialEquation", modelFile).getModel().getInitialResidual())  == str(MX(1)-x1)

def test_OptimicaFunctionCallEquations():
    assert( repr(transferOptimizationProblemWithoutInlining("AtomicModelFunctionCallEquation", modelFile).getModel().getDaeResidual()) == 
                ("MX(vertcat((x1-der_x1),(vertcat(function(\"AtomicModelFunctionCallEquation.f\").call([x1]){0}," +
                 "function(\"AtomicModelFunctionCallEquation.f\").call([x1]){1})-vertcat(x2,x3))))") )  

def test_OptimicaBindingExpression():
    model =  transferOptimizationProblem("AtomicModelAttributeBindingExpression", modelFile).getModel()
    dependent =  model.getVariableByKind(Model.REAL_PARAMETER_DEPENDENT)
    independent =  model.getVariableByKind(Model.REAL_PARAMETER_INDEPENDENT)
    actual =  str(independent[0].getAttribute("bindingExpression")) + str(dependent[0].getAttribute("bindingExpression"))
    expected = str(MX(2)) + str(MX("p1"))
    assert actual == expected

def test_OptimicaUnit():
    model =  transferOptimizationProblem("AtomicModelAttributeUnit", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("unit")) == str(MX("kg")) 

def test_OptimicaQuantity():
    model =  transferOptimizationProblem("AtomicModelAttributeQuantity", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("quantity")) == str(MX("kg")) 

def test_OptimicaDisplayUnit():
    model =  transferOptimizationProblem("AtomicModelAttributeDisplayUnit", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("displayUnit")) == str(MX("kg")) 

def test_OptimicaMin():
    model =  transferOptimizationProblem("AtomicModelAttributeMin", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str((diffs[0].getAttribute("min"))) == str(MX(0)) 

def test_OptimicaMax():
    model =  transferOptimizationProblem("AtomicModelAttributeMax", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("max")) == str(MX(100))
    
def test_OptimicaStart():
    model =  transferOptimizationProblem("AtomicModelAttributeStart", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("start"))  == str(MX(0.0005))
    
def test_OptimicaFixed():
    model =  transferOptimizationProblem("AtomicModelAttributeFixed", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("fixed")) == str(MX(True))

def test_OptimicaNominal():
    model =  transferOptimizationProblem("AtomicModelAttributeNominal", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("nominal")) == str(MX(0.1))
        
def test_OptimicaComment():
    model =  transferOptimizationProblem("AtomicModelComment", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diffs[0].getAttribute("comment")) == str(MX("I am x1's comment"))
        
def test_OptimicaRealDeclaredType():
    model =  transferOptimizationProblem("AtomicModelDerivedRealTypeVoltage", modelFile).getModel()
    assert str(model.getVariableTypeByName("Voltage")) == ("Type name: Voltage, base type: Real, attributes:" +
                                                           "\n\tquantity = MX(ElectricalPotential)\n\tunit = MX(V)")
def test_OptimicaDerivedTypeDefaultType():
    model =  transferOptimizationProblem("AtomicModelDerivedTypeAndDefaultType", modelFile).getModel()
    diffs =  model.getVariableByKind(Model.DIFFERENTIATED)
    assert int(diffs[0].getDeclaredType().this) == int(model.getVariableTypeByName("Voltage").this)
    assert int(diffs[1].getDeclaredType().this) == int(model.getVariableTypeByName("Real").this)

def test_OptimicaIntegerDeclaredType():
    model =  transferOptimizationProblem("AtomicModelDerivedIntegerTypeSteps", modelFile).getModel()
    print str(model.getVariableTypeByName("Steps"))
    assert str(model.getVariableTypeByName("Steps")) == ("Type name: Steps, base type: Integer, attributes:"
                                                                "\n\tquantity = MX(steps)")
    
def test_OptimicaBooleanDeclaredType():
    model =  transferOptimizationProblem("AtomicModelDerivedBooleanTypeIsDone", modelFile).getModel()
    print str(model.getVariableTypeByName("IsDone"))
    assert str(model.getVariableTypeByName("IsDone")) == ("Type name: IsDone, base type: Boolean, attributes:" 
                                                           "\n\tquantity = MX(Done)")

def test_OptimicaRealConstant():
    model =  transferOptimizationProblem("atomicModelRealConstant", modelFile).getModel()
    constVars =  model.getVariableByKind(Model.REAL_CONSTANT)
    assert str(constVars[0].getVar()) == str(MX("pi"))
    assertNear(constVars[0].getAttribute("bindingExpression").getValue(), 3.14, 0.0000001)

def test_OptimicaRealIndependentParameter():
    model =  transferOptimizationProblem("atomicModelRealIndependentParameter", modelFile).getModel()
    indepParam =  model.getVariableByKind(Model.REAL_PARAMETER_INDEPENDENT)
    assert str(indepParam[0].getVar()) == str(MX("pi"))
    assertNear(indepParam[0].getAttribute("bindingExpression").getValue(), 3.14, 0.0000001)
        
def test_OptimicaRealDependentParameter():
    model =  transferOptimizationProblem("atomicModelRealDependentParameter", modelFile).getModel()
    depParam =  model.getVariableByKind(Model.REAL_PARAMETER_DEPENDENT)
    indepParam =  model.getVariableByKind(Model.REAL_PARAMETER_INDEPENDENT)
    assert str(2*(indepParam[0].getVar())) == str(depParam[0].getAttribute("bindingExpression"))
    
def test_OptimicaDerivative():
    model =  transferOptimizationProblem("atomicModelRealDerivative", modelFile).getModel()
    assert str(model.getVariableByKind(Model.DERIVATIVE)[0].getVar()) == str(der_x1)
    
def test_OptimicaDifferentiated():
    model = transferOptimizationProblem("atomicModelRealDifferentiated", modelFile).getModel()
    diff = model.getVariableByKind(Model.DIFFERENTIATED)
    assert str(diff[0].getVar()) == str(x1)
        
def test_OptimicaRealInput():
    model =  transferOptimizationProblem("atomicModelRealInput", modelFile).getModel()
    ins =  model.getVariableByKind(Model.REAL_INPUT)
    assert str(ins[0].getVar()) == str(x1)

def test_OptimicaAlgebraic():
    model =  transferOptimizationProblem("atomicModelRealAlgebraic", modelFile).getModel()
    alg =  model.getVariableByKind(Model.REAL_ALGEBRAIC)
    assert str(alg[0].getVar()) == str(x1)
    
def test_OptimicaRealDisrete():
    model =  transferOptimizationProblem("atomicModelRealDiscrete", modelFile).getModel()
    realDisc =  model.getVariableByKind(Model.REAL_DISCRETE)
    assert str(realDisc[0].getVar()) == str(x1)
    
def test_OptimicaIntegerConstant():
    model =  transferOptimizationProblem("atomicModelIntegerConstant", modelFile).getModel()
    constVars =  model.getVariableByKind(Model.INTEGER_CONSTANT)
    assert str(constVars[0].getVar()) == str(MX("pi"))
    assertNear( constVars[0].getAttribute("bindingExpression").getValue(), 3, 0.0000001)
    
def test_OptimicaIntegerIndependentParameter():
    model =  transferOptimizationProblem("atomicModelIntegerIndependentParameter", modelFile).getModel()
    indepParam =  model.getVariableByKind(Model.INTEGER_PARAMETER_INDEPENDENT)
    assert str(indepParam[0].getVar()) == str(MX("pi"))
    assertNear( indepParam[0].getAttribute("bindingExpression").getValue(), 3, 0.0000001 )
    
def test_OptimicaIntegerDependentConstants():
    model =  transferOptimizationProblem("atomicModelIntegerDependentParameter", modelFile).getModel()
    depParam =  model.getVariableByKind(Model.INTEGER_PARAMETER_DEPENDENT)
    indepParam =  model.getVariableByKind(Model.INTEGER_PARAMETER_INDEPENDENT)
    assert str(2*(indepParam[0].getVar())) == str(depParam[0].getAttribute("bindingExpression"))

def test_OptimicaIntegerDiscrete():
    model =  transferOptimizationProblem("atomicModelIntegerDiscrete", modelFile).getModel()
    intDisc =  model.getVariableByKind(Model.INTEGER_DISCRETE)
    assert str(intDisc[0].getVar()) == str(x1)
    
def test_OptimicaIntegerInput():
    model =  transferOptimizationProblem("atomicModelIntegerInput", modelFile).getModel()
    intIns =  model.getVariableByKind(Model.INTEGER_INPUT)
    assert str(intIns[0].getVar()) == str(x1)
    
def test_OptimicaBooleanConstant():
    model =  transferOptimizationProblem("atomicModelBooleanConstant", modelFile).getModel()
    constVars =  model.getVariableByKind(Model.BOOLEAN_CONSTANT)
    assert str(constVars[0].getVar()) == str(MX("pi"))
    assertNear( constVars[0].getAttribute("bindingExpression").getValue(), MX(True).getValue(), 0.0000001 )
    
def test_OptimicaBooleanIndependentParameter():
    model =  transferOptimizationProblem("atomicModelBooleanIndependentParameter", modelFile).getModel()
    indepParam =  model.getVariableByKind(Model.BOOLEAN_PARAMETER_INDEPENDENT)
    assert str(indepParam[0].getVar()) == str(MX("pi"))
    assertNear( indepParam[0].getAttribute("bindingExpression").getValue(), MX(True).getValue(), 0.0000001 )
    
def test_OptimicaBooleanDependentParameter():
    model =  transferOptimizationProblem("atomicModelBooleanDependentParameter", modelFile).getModel()
    depParam =  model.getVariableByKind(Model.BOOLEAN_PARAMETER_DEPENDENT)
    indepParam =  model.getVariableByKind(Model.BOOLEAN_PARAMETER_INDEPENDENT)
    print depParam[0].getAttribute("bindingExpression")
    assert str( indepParam[0].getVar().logic_and(MX(True)) ) == str(depParam[0].getAttribute("bindingExpression"))
    
def test_OptimicaBooleanDiscrete():
    model =  transferOptimizationProblem("atomicModelBooleanDiscrete", modelFile).getModel()        
    boolDisc =  model.getVariableByKind(Model.BOOLEAN_DISCRETE)
    assert str(boolDisc[0].getVar()) == str(x1)

def test_OptimicaBooleanInput():
    model =  transferOptimizationProblem("atomicModelBooleanInput", modelFile).getModel()
    boolIns =  model.getVariableByKind(Model.BOOLEAN_INPUT)
    assert str(boolIns[0].getVar()) == str(x1)
        
def test_OptimicaModelFunction():
    model =  transferOptimizationProblem("simpleModelWithFunctions", "../common/modelicaModels.mo").getModel()
    expectedPrint = ("ModelFunction : function(\"simpleModelWithFunctions.f\")\n Inputs (2):\n"
                            "  0. 1-by-1 (dense)\n"
                            "  1. 1-by-1 (dense)\n"
                            " Outputs (2):\n"
                            "  0. 1-by-1 (dense)\n"
                            "  1. 1-by-1 (dense)\n"
                            "@0 = input[0]\n"
                            "@1 = input[1]\n"
                            "{@2,@3} = function(\"simpleModelWithFunctions.f2\").call([@0,@1])\n"
                            "output[0] = @2\n"
                            "output[1] = @3\n"
                            "ModelFunction : function(\"simpleModelWithFunctions.f2\")\n Inputs (2):\n"
                            "  0. 1-by-1 (dense)\n"
                            "  1. 1-by-1 (dense)\n"
                            " Outputs (2):\n"
                            "  0. 1-by-1 (dense)\n"
                            "  1. 1-by-1 (dense)\n" 
                            "@0 = Const<0.5>(scalar)\n"
                            "@1 = input[0]\n"
                            "@0 = (@0*@1)\n"
                            "output[0] = @0\n"
                            "@2 = input[1]\n"
                            "@0 = (@2+@0)\n"
                            "output[1] = @0\n")
    mf_1 = model.getModelFunctionByName("simpleModelWithFunctions.f")
    mf_2 = model.getModelFunctionByName("simpleModelWithFunctions.f2")
    actual = str(mf_1) + str(mf_2)
    assert expectedPrint == actual

def test_OptimicaDependentParametersCalculated():
    model =  transferOptimizationProblem("atomicModelDependentParameter", modelFile).getModel()
    model.calculateValuesForDependentParameters()
    depVars = model.getVariableByKind(Model.REAL_PARAMETER_DEPENDENT)
    assert depVars[0].getAttribute("evaluatedBindingExpression").getValue() == 20
    assert depVars[1].getAttribute("evaluatedBindingExpression").getValue() == 20
    assert depVars[2].getAttribute("evaluatedBindingExpression").getValue() == 200


def test_OptimicaFunctionCallEquationForParameterBinding():
    model =  transferOptimizationProblemWithoutInlining("atomicModelPolyOutFunctionCallForDependentParameter", modelFile).getModel()
    model.calculateValuesForDependentParameters()
    expected = ("MX(temp_1[1]), declaredType : Real, attributes:\n"
                "\tbindingExpression = MX(function(\"atomicModelPolyOutFunctionCallForDependentParameter.f\").call([p1]){0})\n"
                "\tevaluatedBindingExpression = MX(Const<2>(scalar))\n"
                "MX(temp_1[2]), declaredType : Real, attributes:\n"
                "\tbindingExpression = MX(function(\"atomicModelPolyOutFunctionCallForDependentParameter.f\").call([p1]){1})\n"
                "\tevaluatedBindingExpression = MX(Const<4>(scalar))\n"
                "MX(p2[1]), declaredType : Real, attributes:\n"
                "\tbindingExpression = MX(temp_1[1])\n"
                "\tevaluatedBindingExpression = MX(Const<2>(scalar))\n"
                "MX(p2[2]), declaredType : Real, attributes:\n"
                "\tbindingExpression = MX(temp_1[2])\n"
                "\tevaluatedBindingExpression = MX(Const<4>(scalar))\n")
    actual = ""
    for var in model.getVariableByKind(Model.REAL_PARAMETER_DEPENDENT):
        actual += str(var) + "\n"
    print actual
    print expected
    assert actual == expected

##############################################
#                                            # 
#         CONSTRUCTS TRANSFER TESTS          #
#                                            #
##############################################


def test_ConstructElementaryExpression():
    dae = transferModelicaModel("AtomicModelElementaryExpressions", modelFile).getDaeResidual()
    expected = "MX(vertcat(((Const<2>(scalar)+x1)-der_x1),((x2-x1)-der_x2),((x3*x2)-der_x3),((x4/x3)-der_x4)))"
    assert repr(dae) == expected 
    
def test_ConstructElementaryFunctions():
    dae = transferModelicaModel("AtomicModelElementaryFunctions", modelFile).getDaeResidual()
    expected = ("MX(vertcat((pow(x1,Const<5>(scalar))-der_x1),(fabs(x2)-der_x2),(fmin(x3,x2)-der_x3)," +
                "(fmax(x4,x3)-der_x4),(sqrt(x5)-der_x5),(sin(x6)-der_x6),(cos(x7)-der_x7),(tan(x8)-der_x8)," +
                "(asin(x9)-der_x9),(acos(x10)-der_x10),(atan(x11)-der_x11),(atan2(x12,x11)-der_x12)," +
                "(sinh(x13)-der_x13),(cosh(x14)-der_x14),(tanh(x15)-der_x15),(exp(x16)-der_x16),(log(x17)-der_x17)," +
                "((Const<0.434294>(scalar)*log(x18))-der_x18),((-x18)-der_x19)))" ) # CasADi converts log10 to log with constant.
    assert repr(dae) == expected
    
def test_ConstructBooleanExpressions():
    dae = transferModelicaModel("AtomicModelBooleanExpressions", modelFile).getDaeResidual()
    expected = ("MX(vertcat((((x2?Const<1>(scalar):0)+((!x2)?Const<2>(scalar):0))-der_x1)," + 
                "((Const<0>(scalar)<x1)-x2),((Const<0>(scalar)<=x1)-x3),((x1<Const<0>(scalar))-x4)" +
                ",((x1<=Const<0>(scalar))-x5),((x5==x4)-x6),((x6!=x5)-x7),((x6&&x5)-x8),((x6||x5)-x9)))" )
    assert repr(dae) == expected
     
def test_ConstructMisc():
    model = transferModelicaModel("AtomicModelMisc", modelFile)
    expected = ("MX(vertcat((Const<1.11>(scalar)-der_x1),(((x3?Const<3>(scalar):0)+((!x3)?Const<4>(scalar):0))-x2)," +
                "((Const<1>(scalar)||(Const<1>(scalar)<x2))-x3),((Const<0>(scalar)||x3)-x4)))" + 
                "MX(vertcat((-x1),(-pre_x2),(-pre_x3),(-pre_x4)))")
    assert (repr(model.getDaeResidual()) + repr(model.getInitialResidual()))  == expected
     
def test_ConstructVariableLaziness():
    model = transferModelicaModel("AtomicModelVariableLaziness", modelFile)
    x2_eq = model.getDaeResidual()[0].getDep(0)
    x1_eq = model.getDaeResidual()[1].getDep(0)
    x1_var = model.getVariableByKind(Model.DIFFERENTIATED)[0].getVar()
    x2_var = model.getVariableByKind(Model.DIFFERENTIATED)[1].getVar()
    assert x1_var.isEqual(x1_eq) and x2_var.isEqual(x2_eq)
    
def test_ConstructArrayInOutFunction1():
    model = transferModelicaModelWithoutInlining("AtomicModelVector1", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelVector1.f\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@0 = (-@0)\n"
                "output[0] = @0\n"
                "@1 = input[1]\n"
                "@1 = (-@1)\n"
                "output[1] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelVector1.f")) == expected
    expected = ("vertcat((vertcat(function(\"AtomicModelVector1.f\").call([A[1],A[2]]){0}," +                                                             
                "function(\"AtomicModelVector1.f\").call([A[1],A[2]]){1})-vertcat(temp_1[1],temp_1[2]))," +
                "(temp_1[1]-der_A[1]),(temp_1[2]-der_A[2]))")
    assert str(model.getDaeResidual()) == expected
 
def test_ConstructArrayInOutFunction2():
    model = transferModelicaModelWithoutInlining("AtomicModelVector2", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelVector2.f\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@1 = input[1]\n"
                "{@2,@3} = function(\"AtomicModelVector2.f2\").call([@0,@1])\n"
                "output[0] = @2\n"
                "output[1] = @3\n")
    assert str(model.getModelFunctionByName("AtomicModelVector2.f")) == expected
    expected = ("vertcat((vertcat(function(\"AtomicModelVector2.f\").call([A[1],A[2]]){0}," +
                "function(\"AtomicModelVector2.f\").call([A[1],A[2]]){1})-vertcat(temp_1[1],temp_1[2]))," +
                "(temp_1[1]-der_A[1]),(temp_1[2]-der_A[2]))")
    assert str(model.getDaeResidual()) == expected
    
def test_ConstructArrayInOutFunctionCallEquation():
    model = transferModelicaModelWithoutInlining("AtomicModelVector3", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelVector3.f\")\n"
                " Inputs (4):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                " Outputs (4):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@0 = (-@0)\n"
                "output[0] = @0\n"
                "@1 = input[1]\n"
                "@1 = (-@1)\n"
                "output[1] = @1\n"
                "@2 = input[2]\n"
                "@2 = (2.*@2)\n"
                "output[2] = @2\n"
                "@3 = input[3]\n"
                "@3 = (2.*@3)\n"
                "output[3] = @3\n")
    assert str(model.getModelFunctionByName("AtomicModelVector3.f")) == expected
    expected = ("(vertcat(function(\"AtomicModelVector3.f\").call([A[1],A[2],Const<1>(scalar),Const<2>(scalar)])" +
                "{0},function(\"AtomicModelVector3.f\").call([A[1],A[2],Const<1>(scalar),Const<2>(scalar)])" +
                "{1},function(\"AtomicModelVector3.f\").call([A[1],A[2],Const<1>(scalar),Const<2>(scalar)]){2}," +
                "function(\"AtomicModelVector3.f\").call([A[1],A[2],Const<1>(scalar),Const<2>(scalar)]){3})-vertcat(A[1],A[2],B[1],B[2]))")
    assert str(model.getDaeResidual()) == expected
    
def test_FunctionCallEquationOmittedOuts():
    model = transferModelicaModelWithoutInlining("atomicModelFunctionCallEquationIgnoredOuts", modelFile)
    expected = ("vertcat(((x1+x2)-der_x2),"
                "(vertcat("
                "function(\"atomicModelFunctionCallEquationIgnoredOuts.f\").call([Const<1>(scalar),x3]){0},"
                "function(\"atomicModelFunctionCallEquationIgnoredOuts.f\").call([Const<1>(scalar),x3]){2})"
                "-vertcat(x1,x2)))")
    assert str(model.getDaeResidual()) == expected
    
def test_FunctionCallStatementOmittedOuts():
    model = transferModelicaModelWithoutInlining("atomicModelFunctionCallStatementIgnoredOuts", modelFile)
    expected = ("ModelFunction : function(\"atomicModelFunctionCallStatementIgnoredOuts.f2\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = Const<10>(scalar)\n"
                "@1 = input[0]\n"
                "{NULL,NULL,@2} = function(\"atomicModelFunctionCallStatementIgnoredOuts.f\").call([@0,@1])\n"
                "output[0] = @2\n")
    assert str(model.getModelFunctionByName("atomicModelFunctionCallStatementIgnoredOuts.f2")) == expected
    
def test_ConstructFunctionMatrix():
    model = transferModelicaModelWithoutInlining("AtomicModelMatrix", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelMatrix.f\")\n"
                " Inputs (4):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[2]\n"
                "output[0] = @0\n"
                "@1 = input[3]\n"
                "output[1] = @1\n"
                "@2 = input[0]\n"
                "@3 = input[1]\n")
    assert str(model.getModelFunctionByName("AtomicModelMatrix.f")) == expected
    expected = ("vertcat((vertcat(function(\"AtomicModelMatrix.f\").call([A[1,1],A[1,2],Const<0.1>(scalar)," +
                "Const<0.3>(scalar)]){0},function(\"AtomicModelMatrix.f\").call([A[1,1],A[1,2],Const<0.1>(scalar)" +
                ",Const<0.3>(scalar)]){1})-vertcat(temp_1[1,1],temp_1[1,2])),((-temp_1[1,1])-der_A[1,1]),((-temp_1[1,2])-der_A[1,2])," +
                "(vertcat(function(\"AtomicModelMatrix.f2\").call([dx[1,1],dx[1,2],dx[2,1],dx[2,2]]){0}," +
                "function(\"AtomicModelMatrix.f2\").call([dx[1,1],dx[1,2],dx[2,1],dx[2,2]]){1}," +
                "function(\"AtomicModelMatrix.f2\").call([dx[1,1],dx[1,2],dx[2,1],dx[2,2]]){2}," +
                "function(\"AtomicModelMatrix.f2\").call([dx[1,1],dx[1,2],dx[2,1],dx[2,2]]){3})-" +
                "vertcat(temp_2[1,1],temp_2[1,2],temp_2[2,1],temp_2[2,2])),((-temp_2[1,1])-der_dx[1,1])," +
                "((-temp_2[1,2])-der_dx[1,2]),((-temp_2[2,1])-der_dx[2,1]),((-temp_2[2,2])-der_dx[2,2]))")
    assert str(model.getDaeResidual()) == expected
        
def test_ConstructFunctionMatrixDimsGreaterThanTwo():
    model = transferModelicaModelWithoutInlining("AtomicModelLargerThanTwoDimensionArray", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelLargerThanTwoDimensionArray.f\")\n"
                " Inputs (6):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                "  4. 1-by-1 (dense)\n"
                "  5. 1-by-1 (dense)\n"
                " Outputs (6):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                "  4. 1-by-1 (dense)\n"
                "  5. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@0 = (-@0)\n"
                "output[0] = @0\n"
                "@1 = input[1]\n"
                "@1 = (-@1)\n"
                "output[1] = @1\n"
                "@2 = input[2]\n"
                "@2 = (-@2)\n"
                "output[2] = @2\n"
                "@3 = input[3]\n"
                "@3 = (-@3)\n"
                "output[3] = @3\n"
                "@4 = input[4]\n"
                "@4 = (-@4)\n"
                "output[4] = @4\n"
                "@5 = Const<10>(scalar)\n"
                "output[5] = @5\n"
                "@6 = input[5]\n")
    assert str(model.getModelFunctionByName("AtomicModelLargerThanTwoDimensionArray.f")) == expected
    expected = ("vertcat((vertcat("
                "function(\"AtomicModelLargerThanTwoDimensionArray.f\").call([A[1,1,1],A[1,1,2],A[1,1,3],A[1,2,1],A[1,2,2],A[1,2,3]]){0}," 
                "function(\"AtomicModelLargerThanTwoDimensionArray.f\").call([A[1,1,1],A[1,1,2],A[1,1,3],A[1,2,1],A[1,2,2],A[1,2,3]]){1}," 
                "function(\"AtomicModelLargerThanTwoDimensionArray.f\").call([A[1,1,1],A[1,1,2],A[1,1,3],A[1,2,1],A[1,2,2],A[1,2,3]]){2}," 
                "function(\"AtomicModelLargerThanTwoDimensionArray.f\").call([A[1,1,1],A[1,1,2],A[1,1,3],A[1,2,1],A[1,2,2],A[1,2,3]]){3},"  
                "function(\"AtomicModelLargerThanTwoDimensionArray.f\").call([A[1,1,1],A[1,1,2],A[1,1,3],A[1,2,1],A[1,2,2],A[1,2,3]]){4}," 
                "function(\"AtomicModelLargerThanTwoDimensionArray.f\").call([A[1,1,1],A[1,1,2],A[1,1,3],A[1,2,1],A[1,2,2],A[1,2,3]]){5})" 
                "-vertcat(temp_1[1,1,1],temp_1[1,1,2],temp_1[1,1,3],temp_1[1,2,1],temp_1[1,2,2],temp_1[1,2,3]))," +
                "(temp_1[1,1,1]-der_A[1,1,1]),(temp_1[1,1,2]-der_A[1,1,2]),(temp_1[1,1,3]-der_A[1,1,3]),(temp_1[1,2,1]-der_A[1,2,1]),(temp_1[1,2,2]-der_A[1,2,2]),(temp_1[1,2,3]-der_A[1,2,3]))")
    assert str(model.getDaeResidual()) == expected
        
def test_ConstructNestedRecordFunctions():
    model = transferModelicaModelWithoutInlining("AtomicModelRecordNestedArray", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelRecordNestedArray.generateCurves\")\n"
                " Input: 1-by-1 (dense)\n"
                " Outputs (8):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                "  4. 1-by-1 (dense)\n"
                "  5. 1-by-1 (dense)\n"
                "  6. 1-by-1 (dense)\n"
                "  7. 1-by-1 (dense)\n"
                "@0 = Const<0>(scalar)\n"
                "output[0] = @0\n"
                "@1 = input[0]\n"
                "output[1] = @1\n"
                "@2 = Const<2>(scalar)\n"
                "output[2] = @2\n"
                "@3 = Const<3>(scalar)\n"
                "output[3] = @3\n"
                "@4 = Const<6>(scalar)\n"
                "output[4] = @4\n"
                "@5 = Const<7>(scalar)\n"
                "output[5] = @5\n"
                "output[6] = @2\n"
                "output[7] = @3\n")
    assert str(model.getModelFunctionByName("AtomicModelRecordNestedArray.generateCurves")) == expected
    expected = ("vertcat((vertcat(" +
                "function(\"AtomicModelRecordNestedArray.generateCurves\").call([a]){0}," +
                "function(\"AtomicModelRecordNestedArray.generateCurves\").call([a]){1}," +
                "function(\"AtomicModelRecordNestedArray.generateCurves\").call([a]){2}," +
                "function(\"AtomicModelRecordNestedArray.generateCurves\").call([a]){3}," +
                "function(\"AtomicModelRecordNestedArray.generateCurves\").call([a]){4}," +
                "function(\"AtomicModelRecordNestedArray.generateCurves\").call([a]){5}," +
                "function(\"AtomicModelRecordNestedArray.generateCurves\").call([a]){6}," +
                "function(\"AtomicModelRecordNestedArray.generateCurves\").call([a]){7})" +
                "-vertcat(" +
                "compCurve.curves[1].path[1].point[1],compCurve.curves[1].path[1].point[2]," + 
                "compCurve.curves[1].path[2].point[1],compCurve.curves[1].path[2].point[2]," +
                "compCurve.curves[2].path[1].point[1],compCurve.curves[2].path[1].point[2]," +
                "compCurve.curves[2].path[2].point[1],compCurve.curves[2].path[2].point[2]))," +
                "(compCurve.curves[1].path[1].point[2]-der_a))")
    assert str(model.getDaeResidual()) == expected
        
def test_ConstructRecordInFunctionInFunction():
    model = transferModelicaModelWithoutInlining("AtomicModelRecordInOutFunctionCallStatement", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelRecordInOutFunctionCallStatement.f1\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = Const<2>(scalar)\n"
                "@1 = input[0]\n"
                "@0 = (@0+@1)\n"
                "{@2,@3} = function(\"AtomicModelRecordInOutFunctionCallStatement.f2\").call([@1,@0])\n"
                "@3 = (@2*@3)\n"
                "output[0] = @3\n"
                "ModelFunction : function(\"AtomicModelRecordInOutFunctionCallStatement.f2\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n"
                "@1 = Const<10>(scalar)\n"
                "@2 = input[1]\n"
                "@2 = (@1*@2)\n" 
                "output[1] = @2\n")
    funcStr = str(model.getModelFunctionByName("AtomicModelRecordInOutFunctionCallStatement.f1")) + str(model.getModelFunctionByName("AtomicModelRecordInOutFunctionCallStatement.f2"))
    assert funcStr == expected
    assert str(model.getDaeResidual()) == "((-function(\"AtomicModelRecordInOutFunctionCallStatement.f1\").call([a]){0})-der_a)"

def test_ConstructRecordArbitraryDimension():
    model = transferModelicaModelWithoutInlining("AtomicModelRecordArbitraryDimension", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelRecordArbitraryDimension.f\")\n"
                " Input: 1-by-1 (dense)\n"
                " Outputs (8):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                "  4. 1-by-1 (dense)\n"
                "  5. 1-by-1 (dense)\n"
                "  6. 1-by-1 (dense)\n"
                "  7. 1-by-1 (dense)\n"
                "@0 = Const<1>(scalar)\n"
                "output[0] = @0\n"
                "@1 = Const<2>(scalar)\n"
                "output[1] = @1\n"
                "@2 = Const<3>(scalar)\n"
                "output[2] = @2\n"
                "@3 = Const<4>(scalar)\n"
                "output[3] = @3\n"
                "@4 = Const<5>(scalar)\n"
                "output[4] = @4\n"
                "@5 = Const<6>(scalar)\n"
                "output[5] = @5\n"
                "@6 = input[0]\n"
                "output[6] = @6\n"
                "@6 = (2.*@6)\n"
                "output[7] = @6\n")
    assert str(model.getModelFunctionByName("AtomicModelRecordArbitraryDimension.f")) == expected
    expected = ("vertcat(((-a)-der_a),(vertcat(" + 
                "function(\"AtomicModelRecordArbitraryDimension.f\").call([a]){0}," +
                "function(\"AtomicModelRecordArbitraryDimension.f\").call([a]){1}," +
                "function(\"AtomicModelRecordArbitraryDimension.f\").call([a]){2}," + 
                "function(\"AtomicModelRecordArbitraryDimension.f\").call([a]){3}," +
                "function(\"AtomicModelRecordArbitraryDimension.f\").call([a]){4}," +
                "function(\"AtomicModelRecordArbitraryDimension.f\").call([a]){5}," +
                "function(\"AtomicModelRecordArbitraryDimension.f\").call([a]){6}," +
                "function(\"AtomicModelRecordArbitraryDimension.f\").call([a]){7})" +
                "-vertcat(r.A[1,1,1],r.A[1,1,2],r.A[1,2,1],r.A[1,2,2],r.A[2,1,1],r.A[2,1,2],r.A[2,2,1],r.A[2,2,2])))")
    assert str(model.getDaeResidual()) == expected
    
def test_ConstructArrayFlattening():
    model =  transferModelicaModelWithoutInlining("atomicModelSimpleArrayIndexing", modelFile)
    model.calculateValuesForDependentParameters()
    expected = ("ModelFunction : function(\"atomicModelSimpleArrayIndexing.f\")\n"
                " Inputs (0):\n"
                " Outputs (4):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                "@0 = Const<1>(scalar)\n"
                "output[0] = @0\n"
                "@1 = Const<2>(scalar)\n"
                "output[1] = @1\n"
                "@2 = Const<3>(scalar)\n"
                "output[2] = @2\n"
                "@3 = Const<4>(scalar)\n"
                "output[3] = @3\n")
    assert str(model.getModelFunctionByName("atomicModelSimpleArrayIndexing.f")) == expected
    
def test_ConstructRecordNestedSeveralVars():
    model = transferModelicaModelWithoutInlining("AtomicModelRecordSeveralVars", modelFile)
    expected = ("ModelFunction : function(\"AtomicModelRecordSeveralVars.f\")\n"
                " Input: 1-by-1 (dense)\n"
                " Outputs (10):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "  2. 1-by-1 (dense)\n"
                "  3. 1-by-1 (dense)\n"
                "  4. 1-by-1 (dense)\n"
                "  5. 1-by-1 (dense)\n"
                "  6. 1-by-1 (dense)\n"
                "  7. 1-by-1 (dense)\n"
                "  8. 1-by-1 (dense)\n"
                "  9. 1-by-1 (dense)\n"
                "@0 = Const<1>(scalar)\n"
                "output[0] = @0\n"
                "@1 = Const<2>(scalar)\n"
                "output[1] = @1\n"
                "@2 = Const<3>(scalar)\n"
                "output[2] = @2\n"
                "@3 = Const<4>(scalar)\n"
                "output[3] = @3\n"
                "@4 = Const<5>(scalar)\n"
                "output[4] = @4\n"
                "@5 = Const<6>(scalar)\n"
                "output[5] = @5\n"
                "@6 = Const<7>(scalar)\n"
                "output[6] = @6\n"
                "@7 = Const<8>(scalar)\n"
                "output[7] = @7\n"
                "@8 = Const<9>(scalar)\n"
                "output[8] = @8\n"
                "@9 = input[0]\n"
                "output[9] = @9\n")
    assert str(model.getModelFunctionByName("AtomicModelRecordSeveralVars.f")) == expected
    expected = ("vertcat(((-a)-der_a),(vertcat(" +  
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){0}," + 
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){1}," +
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){2}," +
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){3}," +
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){4}," +
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){5}," + 
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){6}," +
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){7}," +
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){8}," +
                "function(\"AtomicModelRecordSeveralVars.f\").call([a]){9})" +
                "-vertcat(r.r1.A,r.r1.B,r.rArr[1].A,r.rArr[1].B,r.rArr[2].A,r.rArr[2].B,r.matrix[1,1],r.matrix[1,2],r.matrix[2,1],r.matrix[2,2])))")
    assert str(model.getDaeResidual()) == expected

def test_ConstructFunctionsInRhs():
    model = transferModelicaModelWithoutInlining("AtomicModelAtomicRealFunctions", modelFile)
    expected = ("vertcat((sin(function(\"AtomicModelAtomicRealFunctions.monoInMonoOut\").call([x1]){0})-der_x1),"
                "(function(\"AtomicModelAtomicRealFunctions.polyInMonoOut\").call([x1,x2]){0}-der_x2),"
                "(vertcat(function(\"AtomicModelAtomicRealFunctions.monoInPolyOut\").call([x2]){0},function(\"AtomicModelAtomicRealFunctions.monoInPolyOut\").call([x2]){1})-vertcat(x3,x4)),"
                "(vertcat(function(\"AtomicModelAtomicRealFunctions.polyInPolyOut\").call([x1,x2]){0},function(\"AtomicModelAtomicRealFunctions.polyInPolyOut\").call([x1,x2]){1})-vertcat(x5,x6)),"
                "(function(\"AtomicModelAtomicRealFunctions.monoInMonoOutReturn\").call([x7]){0}-der_x7),"
                "(function(\"AtomicModelAtomicRealFunctions.functionCallInFunction\").call([x8]){0}-der_x8),"
                "(function(\"AtomicModelAtomicRealFunctions.functionCallEquationInFunction\").call([x9]){0}-der_x9),"
                "(function(\"AtomicModelAtomicRealFunctions.monoInMonoOutInternal\").call([x10]){0}-der_x10),"
                "(vertcat(function(\"AtomicModelAtomicRealFunctions.polyInPolyOutInternal\").call([x9,x10]){0},function(\"AtomicModelAtomicRealFunctions.polyInPolyOutInternal\").call([x9,x10]){1})-vertcat(x11,x12)))")
    assert str(model.getDaeResidual()) == expected 
    
    model = transferModelicaModelWithoutInlining("AtomicModelAtomicIntegerFunctions", modelFile)
    expected = ("vertcat(("
                "function(\"AtomicModelAtomicIntegerFunctions.monoInMonoOut\").call([x1]){0}-x1),"
                "(function(\"AtomicModelAtomicIntegerFunctions.polyInMonoOut\").call([x1,x2]){0}-x2),"
                "(vertcat(function(\"AtomicModelAtomicIntegerFunctions.monoInPolyOut\").call([x2]){0},function(\"AtomicModelAtomicIntegerFunctions.monoInPolyOut\").call([x2]){1})-vertcat(x3,x4)),"
                "(vertcat(function(\"AtomicModelAtomicIntegerFunctions.polyInPolyOut\").call([x1,x2]){0},function(\"AtomicModelAtomicIntegerFunctions.polyInPolyOut\").call([x1,x2]){1})-vertcat(x5,x6)),"
                "(function(\"AtomicModelAtomicIntegerFunctions.monoInMonoOutReturn\").call([x7]){0}-x7),"
                "(function(\"AtomicModelAtomicIntegerFunctions.functionCallInFunction\").call([x8]){0}-x8),"
                "(function(\"AtomicModelAtomicIntegerFunctions.functionCallEquationInFunction\").call([x9]){0}-x9),"
                "(function(\"AtomicModelAtomicIntegerFunctions.monoInMonoOutInternal\").call([x10]){0}-x10),"
                "(vertcat(function(\"AtomicModelAtomicIntegerFunctions.polyInPolyOutInternal\").call([x9,x10]){0},function(\"AtomicModelAtomicIntegerFunctions.polyInPolyOutInternal\").call([x9,x10]){1})-vertcat(x11,x12)))")
    assert str(model.getDaeResidual()) == expected 
      
    model = transferModelicaModelWithoutInlining("AtomicModelAtomicBooleanFunctions", modelFile)
    expected = ("vertcat(("
                "function(\"AtomicModelAtomicBooleanFunctions.monoInMonoOut\").call([x1]){0}-x1),"
                "(function(\"AtomicModelAtomicBooleanFunctions.polyInMonoOut\").call([x1,x2]){0}-x2),"
                "(vertcat(function(\"AtomicModelAtomicBooleanFunctions.monoInPolyOut\").call([x2]){0},function(\"AtomicModelAtomicBooleanFunctions.monoInPolyOut\").call([x2]){1})-vertcat(x3,x4)),"
                "(vertcat(function(\"AtomicModelAtomicBooleanFunctions.polyInPolyOut\").call([x1,x2]){0},function(\"AtomicModelAtomicBooleanFunctions.polyInPolyOut\").call([x1,x2]){1})-vertcat(x5,x6)),"
                "(function(\"AtomicModelAtomicBooleanFunctions.monoInMonoOutReturn\").call([x7]){0}-x7),"
                "(function(\"AtomicModelAtomicBooleanFunctions.functionCallInFunction\").call([x8]){0}-x8),"
                "(function(\"AtomicModelAtomicBooleanFunctions.functionCallEquationInFunction\").call([x9]){0}-x9),"
                "(function(\"AtomicModelAtomicBooleanFunctions.monoInMonoOutInternal\").call([x10]){0}-x10),"
                "(vertcat(function(\"AtomicModelAtomicBooleanFunctions.polyInPolyOutInternal\").call([x9,x10]){0},function(\"AtomicModelAtomicBooleanFunctions.polyInPolyOutInternal\").call([x9,x10]){1})-vertcat(x11,x12)))")
    assert str(model.getDaeResidual()) == expected 
     
def test_ConstructVariousRealValuedFunctions():
    model = transferModelicaModelWithoutInlining("AtomicModelAtomicRealFunctions", modelFile)
    #function monoInMonoOut
        #input Real x
        #output Real y
    #algorithm
        #y := x
    #end monoInMonoOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.monoInMonoOut\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.monoInMonoOut")) == expected 

    #function polyInMonoOut
        #input Real x1
        #input Real x2
        #output Real y
    #algorithm
        #y := x1+x2
    #end polyInMonoOut
    #end monoInMonoOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.polyInMonoOut\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@1 = input[1]\n"
                "@1 = (@0+@1)\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.polyInMonoOut")) == expected 

    #function monoInPolyOut
        #input Real x
        #output Real y1
        #output Real y2
    #algorithm
        #y1 := if(x > 2) then 1 else 5
        #y2 := x
    #end monoInPolyOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.monoInPolyOut\")\n"
                " Input: 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = Const<2>(scalar)\n"
                "@1 = input[0]\n"
                "@2 = (@0<@1)\n"
                "@3 = Const<1>(scalar)\n"
                "@3 = (@2?@3:0)\n"
                "@2 = (!@2)\n"
                "@4 = Const<5>(scalar)\n"
                "@4 = (@2?@4:0)\n"
                "@4 = (@3+@4)\n"
                "output[0] = @4\n"
                "output[1] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.monoInPolyOut")) == expected
    
    #function polyInPolyOut
        #input Real x1
        #input Real x2
        #output Real y1
        #output Real y2
    #algorithm
        #y1 := x1
        #y2 := x2
    #end polyInPolyOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.polyInPolyOut\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n"
                "@1 = input[1]\n"
                "output[1] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.polyInPolyOut")) == expected
    
    #function monoInMonoOutReturn
        #input Real x
        #output Real y
    #algorithm
        #y := x
        #return
        #y := 2*x
    #end monoInMonoOutReturn
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.monoInMonoOutReturn\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.monoInMonoOutReturn")) == expected

    #function functionCallInFunction
        #input Real x
        #output Real y
    #algorithm
        #y := monoInMonoOut(x)
    #end functionCallInFunction
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.functionCallInFunction\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@1 = function(\"AtomicModelAtomicRealFunctions.monoInMonoOut\").call([@0])\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.functionCallInFunction")) == expected
    
    #function functionCallEquationInFunction
        #input Real x
        #Real internal
        #output Real y
    #algorithm
        #(y,internal) := monoInPolyOut(x)
    #end functionCallEquationInFunction
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.functionCallEquationInFunction\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "{@1,NULL} = function(\"AtomicModelAtomicRealFunctions.monoInPolyOut\").call([@0])\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.functionCallEquationInFunction")) == expected

    #function monoInMonoOutInternal
        #input Real x
        #Real internal
        #output Real y
    #algorithm
        #internal := sin(x)
        #y := x*internal
        #internal := sin(y)
        #y := x + internal
    #end monoInMonoOutInternal
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.monoInMonoOutInternal\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@1 = sin(@0)\n"
                "@1 = (@0*@1)\n"
                "@1 = sin(@1)\n"
                "@0 = (@0+@1)\n"
                "output[0] = @0\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.monoInMonoOutInternal")) == expected

    #function polyInPolyOutInternal
        #input Real x1
        #input Real x2
        #Real internal1
        #Real internal2
        #output Real y1
        #output Real y2
    #algorithm
        #internal1 := x1
        #internal2 := x2 + internal1
        #y1 := internal1
        #y2 := internal2 + x1
        #y2 := 1
    #end polyInPolyOutInternal
    expected = ("ModelFunction : function(\"AtomicModelAtomicRealFunctions.polyInPolyOutInternal\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n"
                "@1 = Const<1>(scalar)\n"
                "output[1] = @1\n"
                "@2 = input[1]\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicRealFunctions.polyInPolyOutInternal")) == expected
     
     
def test_ConstructVariousIntegerValuedFunctions():
    model = transferModelicaModelWithoutInlining("AtomicModelAtomicIntegerFunctions", modelFile)
    #function monoInMonoOut
        #input Integer x
        #output Integer y
    #algorithm
        #y := x
    #end monoInMonoOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.monoInMonoOut\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.monoInMonoOut")) == expected 

    #function polyInMonoOut
        #input Integer x1
        #input Integer x2
        #output Integer y
    #algorithm
        #y := x1+x2
    #end polyInMonoOut
    #end monoInMonoOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.polyInMonoOut\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@1 = input[1]\n"
                "@1 = (@0+@1)\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.polyInMonoOut")) == expected 

    #function monoInPolyOut
        #input Integer x
        #output Integer y1
        #output Integer y2
    #algorithm
        #y1 := if(x > 2) then 1 else 5
        #y2 := x
    #end monoInPolyOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.monoInPolyOut\")\n"
                " Input: 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = Const<2>(scalar)\n"
                "@1 = input[0]\n"
                "@2 = (@0<@1)\n"
                "@3 = Const<1>(scalar)\n"
                "@3 = (@2?@3:0)\n"
                "@2 = (!@2)\n"
                "@4 = Const<5>(scalar)\n"
                "@4 = (@2?@4:0)\n"
                "@4 = (@3+@4)\n"
                "output[0] = @4\n"
                "output[1] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.monoInPolyOut")) == expected
    
    #function polyInPolyOut
        #input Integer x1
        #input Integer x2
        #output Integer y1
        #output Integer y2
    #algorithm
        #y1 := x1
        #y2 := x2
    #end polyInPolyOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.polyInPolyOut\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n"
                "@1 = input[1]\n"
                "output[1] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.polyInPolyOut")) == expected
    
    #function monoInMonoOutReturn
        #input Integer x
        #output Integer y
    #algorithm
        #y := x
        #return
        #y := 2*x
    #end monoInMonoOutReturn
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.monoInMonoOutReturn\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.monoInMonoOutReturn")) == expected

    #function functionCallInFunction
        #input Integer x
        #output Integer y
    #algorithm
        #y := monoInMonoOut(x)
    #end functionCallInFunction
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.functionCallInFunction\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@1 = function(\"AtomicModelAtomicIntegerFunctions.monoInMonoOut\").call([@0])\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.functionCallInFunction")) == expected
    
    #function functionCallEquationInFunction
        #input Integer x
        #Integer internal
        #output Integer y
    #algorithm
        #(y,internal) := monoInPolyOut(x)
    #end functionCallEquationInFunction
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.functionCallEquationInFunction\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "{@1,NULL} = function(\"AtomicModelAtomicIntegerFunctions.monoInPolyOut\").call([@0])\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.functionCallEquationInFunction")) == expected

    #function monoInMonoOutInternal
        #input Integer x
        #Integer internal
        #output Integer y
    #algorithm
        #internal := 3*x
        #y := x*internal
        #internal := 1+y
        #y := x + internal
    #end monoInMonoOutInternal
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.monoInMonoOutInternal\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = Const<3>(scalar)\n"
                "@1 = input[0]\n"
                "@2 = (@0*@1)\n"
                "@2 = (@1*@2)\n"
                "@3 = Const<1>(scalar)\n"
                "@2 = (@3+@2)\n"
                "@1 = (@1+@2)\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.monoInMonoOutInternal")) == expected

    #function polyInPolyOutInternal
        #input Integer x1
        #input Integer x2
        #Integer internal1
        #Integer internal2
        #output Integer y1
        #output Integer y2
    #algorithm
        #internal1 := x1
        #internal2 := x2 + internal1
        #y1 := internal1
        #y2 := internal2 + x1
        #y2 := 1
    #end polyInPolyOutInternal
    expected = ("ModelFunction : function(\"AtomicModelAtomicIntegerFunctions.polyInPolyOutInternal\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n"
                "@1 = Const<1>(scalar)\n"
                "output[1] = @1\n"
                "@2 = input[1]\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicIntegerFunctions.polyInPolyOutInternal")) == expected
     
     
def test_ConstructVariousBooleanValuedFunctions():
    model = transferModelicaModelWithoutInlining("AtomicModelAtomicBooleanFunctions", modelFile)
    #function monoInMonoOut
        #input Boolean x
        #output Boolean y
    #algorithm
        #y := x
    #end monoInMonoOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.monoInMonoOut\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.monoInMonoOut")) == expected 

    #function polyInMonoOut
        #input Boolean x1
        #input Boolean x2
        #output Boolean y
    #algorithm
        #y := x1 and x2
    #end polyInMonoOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.polyInMonoOut\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@1 = input[1]\n"
                "@1 = (@0&&@1)\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.polyInMonoOut")) == expected 

    #function monoInPolyOut
        #input Boolean x
        #output Boolean y1
        #output Boolean y2
    #algorithm
        #y1 := if(x) then false else (x or false)
        #y2 := x
    #end monoInPolyOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.monoInPolyOut\")\n"
                " Input: 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = Const<0>(scalar)\n"
                "@1 = input[0]\n"
                "@0 = (@0||@1)\n"
                "@2 = (!@1)\n"
                "@0 = (@2?@0:0)\n"
                "output[0] = @0\n"
                "output[1] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.monoInPolyOut")) == expected
    
    #function polyInPolyOut
        #input Boolean x1
        #input Boolean x2
        #output Boolean y1
        #output Boolean y2
    #algorithm
        #y1 := x1
        #y2 := x2
    #end polyInPolyOut
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.polyInPolyOut\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n"
                "@1 = input[1]\n"
                "output[1] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.polyInPolyOut")) == expected
    
    #function monoInMonoOutReturn
        #input Boolean x
        #output Boolean y
    #algorithm
        #y := x
        #return
        #y := x or false
    #end monoInMonoOutReturn
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.monoInMonoOutReturn\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.monoInMonoOutReturn")) == expected

    #function functionCallInFunction
        #input Boolean x
        #output Boolean y
    #algorithm
        #y := monoInMonoOut(x)
    #end functionCallInFunction
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.functionCallInFunction\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@1 = function(\"AtomicModelAtomicBooleanFunctions.monoInMonoOut\").call([@0])\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.functionCallInFunction")) == expected
    
    #function functionCallEquationInFunction
        #input Boolean x
        #Boolean internal
        #output Boolean y
    #algorithm
        #(y,internal) := monoInPolyOut(x)
    #end functionCallEquationInFunction
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.functionCallEquationInFunction\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "{@1,NULL} = function(\"AtomicModelAtomicBooleanFunctions.monoInPolyOut\").call([@0])\n"
                "output[0] = @1\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.functionCallEquationInFunction")) == expected

    #function monoInMonoOutInternal
        #input Boolean x
        #Boolean internal
        #output Boolean y
    #algorithm
        #internal := x
        #y := x and internal
        #internal := false or y
        #y := false or internal
    #end monoInMonoOutInternal
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.monoInMonoOutInternal\")\n"
                " Input: 1-by-1 (dense)\n"
                " Output: 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "@0 = (@0&&@0)\n"
                "@1 = Const<0>(scalar)\n"
                "@0 = (@1||@0)\n"
                "@2 = Const<0>(scalar)\n"
                "@0 = (@2||@0)\n"
                "output[0] = @0\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.monoInMonoOutInternal")) == expected

    #function polyInPolyOutInternal
        #input Boolean x1
        #input Boolean x2
        #Boolean internal1
        #Boolean internal2
        #output Boolean y1
        #output Boolean y2
    #algorithm
        #internal1 := x1
        #internal2 := x2  or internal1
        #y1 := internal1
        #y2 := internal2 or x1
        #y2 := true
    #end polyInPolyOutInternal
    expected = ("ModelFunction : function(\"AtomicModelAtomicBooleanFunctions.polyInPolyOutInternal\")\n"
                " Inputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                " Outputs (2):\n"
                "  0. 1-by-1 (dense)\n"
                "  1. 1-by-1 (dense)\n"
                "@0 = input[0]\n"
                "output[0] = @0\n"
                "@1 = Const<1>(scalar)\n"
                "output[1] = @1\n"
                "@2 = input[1]\n")
    assert str(model.getModelFunctionByName("AtomicModelAtomicBooleanFunctions.polyInPolyOutInternal")) == expected
     
     
