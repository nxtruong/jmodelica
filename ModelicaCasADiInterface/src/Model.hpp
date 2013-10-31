/*
Copyright (C) 2013 Modelon AB

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef _MODELICACASADI_MODEL 
#define _MODELICACASADI_MODEL
#include <symbolic/casadi.hpp>
#include <ModelFunction.hpp>
#include <types/VariableType.hpp>
#include <Variable.hpp>
#include <RealVariable.hpp>
#include <Equation.hpp>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "Printable.hpp"

namespace ModelicaCasADi 
{  
class Model: public Printable {
    private:
        typedef std::map<std::string,ModelFunction*> functionMap;
        typedef std::map<std::string,VariableType*> typeMap;
    public:
        enum VariableKind {
            REAL_CONSTANT,       
            REAL_PARAMETER_INDEPENDENT,                         
            REAL_PARAMETER_DEPENDENT,   
                                  
            INTEGER_CONSTANT,                           
            INTEGER_PARAMETER_INDEPENDENT,                         
            INTEGER_PARAMETER_DEPENDENT,      
                               
            BOOLEAN_CONSTANT,                             
            BOOLEAN_PARAMETER_INDEPENDENT,                         
            BOOLEAN_PARAMETER_DEPENDENT,               
                      
            STRING_CONSTANT,                       
            STRING_PARAMETER_INDEPENDENT,                         
            STRING_PARAMETER_DEPENDENT,                         

            DERIVATIVE,
            DIFFERENTIATED,
            REAL_INPUT, 
            REAL_ALGEBRAIC,
            REAL_DISCRETE,

            INTEGER_DISCRETE,
            INTEGER_INPUT,
            BOOLEAN_DISCRETE,
            BOOLEAN_INPUT,
            STRING_DISCRETE,
            STRING_INPUT,
            OUTPUT,

            NUM_OF_VARIABLE_KIND  // This must be defined last & no other
                                  // variables may be explicitly defined with a number
        }; // End enum VariableKind
        /** A Model is instantiated without any arguments */
        Model();
        /** @param A MX */
        void setTimeVariable(CasADi::MX timeVar);
        /** @return A MX, this Model's time variable */
        CasADi::MX getTimeVariable();
        
        /** 
         * Variables are assigned a default VariableType if they do not have one set. 
         * @param A pointer to a Variable. 
         */
        void addVariable(Variable* var);
        /** @param A pointer to an equation */    
        void addInitialEquation(Equation* eq);
        /** @param A pointer to an equation */ 
        void addDaeEquation(Equation* eq);
        /** @param A pointer to a ModelFunction */
        void setModelFunctionByItsName(ModelFunction* mf);
        /** 
         * Adds a new VariableType. VariableTypes are singletons and all variable 
         * types must have unique names.
         * @param A pointer to a VariableType
         */
        void addNewVariableType(VariableType* type);
        
        /** 
         * @param The name of the type
         * @return A pointer to a VariableType. Returns NULL if not present 
         * */
        VariableType* getVariableTypeByName(std::string typeName) const;

        /** 
         * Get a vector of pointers to variables of a specific kind, as defined in 
         * the VariableKind enum.
         * @param A VariableKind enum
         * @return An std::vector of pointers to Variables
         */
        std::vector<Variable*> getVariableByKind(VariableKind kind);
        
        /** @return A vector of pointers to Variables. */
        std::vector<Variable*> getAllVariables();
        
        /** @return A vector of pointers to all model variables (i.e. that haven't been aliaseliminated). */
        std::vector<Variable*> getModelVariables();
        /** @return A vector of pointers to all alias variables in the model. */
        std::vector<Variable*> getAliasVariables();

        /**
         * Returns the Variable with a certain name in the Model.
         * If there is no variable with the name present NULL is returned.
         * This method does not discriminate between alias variables and
         * an alias variable may be returned.
         * @param String name of a Variable
         * @return A pointer to a Variable
         */
        Variable* getVariableByName(std::string name);
        
        /**
         * Returns the Variable with a certain name in the Model.
         * If there is no variable with the name present NULL is returned.
         * This method does discriminate between alias variables and if the
         * provided name is an alias variable its alias is returned instead. 
         * @param String name of a Variable
         * @return A pointer to a Variable
         */
        Variable* getModelVariableByName(std::string name);
        

        /** Calculates values for dependent parameters */
        void calculateValuesForDependentParameters();
        /**
         * Calculates the value of the supplied expression. Assumes that the 
         * MX in the expression are either parameters or constants present
         * in the Model.
         * @param A MX
         * @return A double
         */
        double evaluateExpression(CasADi::MX exp);        
        
        /** 
         * Returns all initial equations in a stacked MX on the form: rhs - lhs.
         * @return A MX.
         */
        const CasADi::MX getInitialResidual() const; 
        /** 
         * Returns all DAE equations in a stacked MX on the form: rhs - lhs.
         * @return A MX.
         */
        const CasADi::MX getDaeResidual() const; 
        /** 
         * @param The name of the ModelFunction
         * @return A pointer to a ModelFunction. Returns NULL if not present 
         */
        ModelFunction* getModelFunctionByName(std::string name) const; 
        
        /** Allows the use of operator << to print this class, through Printable. */
        virtual void print(std::ostream& os) const;
    private:
        /// The MX for independent parameters and constants. Filled by calculateValuesForDependentParameters.
        std::vector<CasADi::MX> paramAndConstMXVec;
        /// The values for independent parameters and constants. Filled by calculateValuesForDependentParameters. 
        std::vector<double> paramAndConstValVec;
        CasADi::MX timeVar;
        /// Vector containing pointers to all variables.
        std::vector<Variable*> z;  
        /// Vector containing pointers to DAE equations
        std::vector<Equation*> daeEquations; 
        /// Vector containing pointers to all initial equations
        std::vector<Equation*> initialEquations; 
        /// A map for ModelFunction, key is ModelFunction's name.
        functionMap modelFunctionMap;  
        /// For classification according to the VariableKind enum. Differentiated variables may have their 
        /// myDerivativeVariable field set in the process. 
        VariableKind classifyVariable(Variable* var) const; 
        VariableKind classifyInternalRealVariable(Variable* var) const; 
        VariableKind classifyInternalIntegerVariable(Variable* var) const; 
        VariableKind classifyInternalBooleanVariable(Variable* var) const; 
        VariableKind classifyInternalStringVariable(Variable* var) const; 
        VariableKind classifyInputVariable(Variable* var) const;
        VariableKind classifyInternalVariable(Variable* var) const;
        
        bool checkDiff(RealVariable* var) const;
        bool isDifferentiated(RealVariable* var) const;
        
        /// Adds the MX and their values for independent parameters and constants to paramAndConst(Val/MX)Vec
        void setUpValAndSymbolVecs();
        ///  Tries to evaluate the expression exp using values and nodes in paramAnd(ConstMX/Val)Vec
        double evalMX(CasADi::MX exp);
                
        typeMap typesInModel;
        void assignVariableTypeToRealVariable(Variable* var);
        void assignVariableTypeToIntegerVariable(Variable* var);
        void assignVariableTypeToBooleanVariable(Variable* var);
        void handleVariableTypeForAddedVariable(Variable* var);
        void assignVariableTypeToVariable(Variable* var);
};
inline void Model::setTimeVariable(CasADi::MX timeVar) {this->timeVar = timeVar;}
inline CasADi::MX Model::getTimeVariable() {return timeVar;}
inline std::vector<Variable*> Model::getAllVariables() {return z;}
inline Model::Model() : z(), daeEquations(), initialEquations(), modelFunctionMap(), paramAndConstMXVec(), paramAndConstValVec() {}
inline VariableType* Model::getVariableTypeByName(std::string typeName) const { return typesInModel.find(typeName) != typesInModel.end() ? typesInModel.find(typeName)->second : NULL; }
inline void Model::setModelFunctionByItsName(ModelFunction* mf) { modelFunctionMap[mf->getName()] = mf; }
inline ModelFunction* Model::getModelFunctionByName(std::string name) const { return modelFunctionMap.find(name) != modelFunctionMap.end() ? modelFunctionMap.find(name)->second : NULL; }
inline void Model::addInitialEquation(Equation* eq) { initialEquations.push_back(eq); }
inline void Model::addDaeEquation(Equation* eq) { daeEquations.push_back(eq); }
}; // End namespace
#endif
