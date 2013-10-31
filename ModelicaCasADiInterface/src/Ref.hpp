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

#ifndef _MODELICACASADI_REF
#define _MODELICACASADI_REF

#include <cassert>
#include <cstddef>  // for NULL


namespace ModelicaCasADi
{
template <class T> class Ref {
    public:
        // Default constructor needed so that SWIG doesn't use SWIGValueWrapper<Ref<T>>
        Ref() { this->node = NULL; }
        // Non-template versions of constructors and assignment operator needed by SWIG
        Ref(T *node) { this->node = node; incRef(); }
        Ref(const Ref<T> &ref) { this->node = ref.node; incRef(); }
        template <class S> Ref(S *node) { this->node = node; incRef(); }
        template <class S> Ref(const Ref<S> &ref) { this->node = ref.node; incRef(); }
        ~Ref() { decRef(); }
        
        Ref<T>& operator=(T* node) { setNode(node); return *this; }
        Ref<T>& operator=(const Ref<T>& ref) { setNode(ref.node); return *this; }
        template <class S> Ref<T>& operator=(S* node) { setNode(node); return *this; }
        template <class S> Ref<T>& operator=(const Ref<S>& ref) { setNode(ref.node); return *this; }
        
        const T *operator->() const { assert(node != NULL); return node; }
        T *operator->() { assert(node != NULL); return node; }
        
        const T *getNode() const { return node; }
        T *getNode() { return node; }

        void setNode(T *node) {
            if (this->node == node) return;
            
            decRef();
            this->node = node;
            incRef();
        }

        T *node;    
    private:
        void incRef() { incRefNode(node); }
        void decRef() { if (decRefNode(node)) node = NULL; }
};
}; // End namespace
#endif
