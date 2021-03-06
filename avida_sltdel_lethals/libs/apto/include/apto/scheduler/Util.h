/*
 *  Util.h
 *  Apto
 *
 *  Created by David on 10/25/12.
 *  Copyright 2012 David Michael Bryson. All rights reserved.
 *  http://programerror.com/software/apto
 *
 *  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
 *  following conditions are met:
 *
 *  1.  Redistributions of source code must retain the above copyright notice, this list of conditions and the
 *      following disclaimer.
 *  2.  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
 *      following disclaimer in the documentation and/or other materials provided with the distribution.
 *  3.  Neither the name of David Michael Bryson, nor the names of contributors may be used to endorse or promote
 *      products derived from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY DAVID MICHAEL BRYSON AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
 *  INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
 *  DISCLAIMED. IN NO EVENT SHALL DAVID MICHAEL BRYSON OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 *  SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
 *  WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
 *  USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 *  Authors: David M. Bryson <david@programerror.com>
 *
 */

#ifndef AptoSchedulerUtil_h
#define AptoSchedulerUtil_h

#include <cmath>


namespace Apto {
  namespace Scheduler {
    namespace Util {
    
      // Priority - helper class for dissecting priority values
      // --------------------------------------------------------------------------------------------------------------
    
      class Priority
      {
      protected:
        int m_bits;
        unsigned int m_base;
        int m_offset;
        double m_value;
        
      public:
        Priority(double value) : m_value(value)
        {
          static const int max_bits = sizeof(unsigned int) * 8;
          struct ExponentMultiplier
          {
            double mult[max_bits + 1];
            ExponentMultiplier() { for (int i = 0; i <= max_bits; i++) mult[i] = pow(2.0, i - 1); }
          };
          static ExponentMultiplier exp;
          
          // Do not allow negative priorities. If less than 1, set to 0.
          if (m_value < 1.0) m_value = 0.0;
          
          double mant = frexp(m_value, &m_bits);
          
          if (m_bits > max_bits)
            m_offset = m_bits - max_bits;
          else
            m_offset = 0;
          
          m_base = static_cast<unsigned int>(mant * exp.mult[m_bits - m_offset] * 2.0);
        }
        
        inline int Bit(int bit_num)  const
        {
          assert(bit_num >= 0);
          return (bit_num >= m_offset && bit_num < m_bits) ? (m_base >> (bit_num - m_offset) ) & 0x1 : 0;
        }
        
        inline int NumBits() const { return m_bits; }
      };

    };
  };
};

#endif
