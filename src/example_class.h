/**
 * @file example_class.h
 * @author PehotinDO
 */

#ifndef EXAMPLE_CLASS_H_
#define EXAMPLE_CLASS_H_

#include <cstdint>

/**
 * @brief Демонстрационный пример
 *
 */
class ExampleClass
{
	public:
		ExampleClass();
		~ExampleClass() {};

		uint32_t indexMax;

		static uint32_t mask;
		static uint32_t applyMask(uint32_t val);

		uint32_t computeFactorial(uint32_t n);
		uint32_t computeAxpy(uint32_t len, int32_t* dstY, int32_t a, int32_t* srcX, int32_t* srcY);
		uint32_t findIndexMaxElement(uint32_t len, int32_t* val);

		uint32_t mustException(int32_t val);
};

#endif /* EXAMPLE_CLASS_H_ */
