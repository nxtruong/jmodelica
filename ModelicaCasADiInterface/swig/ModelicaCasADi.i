%{
#include "Equation.hpp"
#include "Constraint.hpp"
#include "AttributeExpression.hpp"
#include "ModelFunction.hpp"

#include "types/VariableType.hpp"
#include "types/PrimitiveType.hpp"
#include "types/BooleanType.hpp"
#include "types/IntegerType.hpp"
#include "types/RealType.hpp"
#include "types/UserType.hpp"

#include "Variable.hpp"
#include "RealVariable.hpp"
#include "DerivativeVariable.hpp"
#include "BooleanVariable.hpp"
#include "IntegerVariable.hpp"

#include "Model.hpp"
#include "OptimizationProblem.hpp"

#include "transferModelica.hpp"
#include "transferOptimica.hpp"

#include "CompilerOptionsWrapper.hpp"

#include "SharedNode.hpp"
#include "Ref.hpp"
%}
%include "doc.i"

%rename(MyVariable) ModelicaCasADi::Variable;
%rename(_transferModelicaModel) transferModelicaModel;
%rename(_transferOptimizationProblem) transferOptimizationProblem;


%feature("ref")   SharedNode "ModelicaCasADi::incRefNode($this);"
%feature("unref") SharedNode "ModelicaCasADi::decRefNode($this);"


%include "std_string.i"
%include "std_vector.i"

%template(MyVariableVector) std::vector<ModelicaCasADi::Variable*>;
%template(StringVector) std::vector<std::string>;
%template(ConstraintVector) std::vector<ModelicaCasADi::Constraint>;

// These must be in dependency order!
// SWIG doesn't follow #includes in the header files

%include "Ref.i" // includes Ref.hpp

// Instantiate Ref<T> along with apropriate typemaps
// All %instantiate_Ref invocations must be afer "Ref.i"
// and befor the header for the type T in question.
//%instantiate_Ref(ModelicaCasADi::Equation)


%include "Printable.hpp"
%include "SharedNode.hpp"

%include "Equation.hpp"
%include "Constraint.hpp"
%include "AttributeExpression.hpp"
%include "ModelFunction.hpp"

%include "types/VariableType.hpp"
%include "types/PrimitiveType.hpp"
%include "types/BooleanType.hpp"
%include "types/IntegerType.hpp"
%include "types/RealType.hpp"
%include "types/UserType.hpp"

%include "Variable.hpp"
%include "RealVariable.hpp"
%include "DerivativeVariable.hpp"
%include "BooleanVariable.hpp"
%include "IntegerVariable.hpp"

%include "Model.hpp"
%include "OptimizationProblem.hpp"

%include "sharedTransferFunctionality.hpp"

%include "CompilerOptionsWrapper.hpp"

%include "transferModelica.hpp"
%include "transferOptimica.hpp"

%extend ModelicaCasADi::Equation {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::Constraint {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::ModelFunction {
  std::string __repr__() { return $self->repr(); }
}

%extend ModelicaCasADi::VariableType {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::PrimitiveType {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::BooleanType {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::IntegerType {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::RealType {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::UserType {
  std::string __repr__() { return $self->repr(); }
}

%extend ModelicaCasADi::Variable {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::RealVariable {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::DerivativeVariable {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::BooleanVariable {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::IntegerVariable {
  std::string __repr__() { return $self->repr(); }
}

%extend ModelicaCasADi::Model {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::OptimizationProblem {
  std::string __repr__() { return $self->repr(); }
}
%extend ModelicaCasADi::CompilerOptionsWrapper {
  std::string __repr__() { return $self->repr(); }
}

/*
#ifdef SWIG
    %extend ModelicaCasADi::Printable{
        std::string __repr__() { return $self->repr(); }
    }
#endif
*/
