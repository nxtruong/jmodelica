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

#ifndef _MODELICACASADI_INTEGER_VAR
#define _MODELICACASADI_INTEGER_VAR
#include <Variable.hpp>
namespace ModelicaCasADi
{
class IntegerVariable : public Variable {
    public:
        /**
         * Create an Integer Variable. 
         * An integer Variable may not have continuous variability. 
         * @param A symbolic MX
         * @param A Causality enum
         * @param A Variability enum
         * @param A pointer to a VariableType, dafault is NULL. 
         */ 
        IntegerVariable(CasADi::MX var, Causality causality, 
                     Variability variability,
                     VariableType* declaredType = NULL);
        /** @param The Integer Type enum */
        const Type getType() const;
};
inline const Variable::Type IntegerVariable::getType() const { return Variable::INTEGER; }
}; // End namespace
#endif
