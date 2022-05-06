/**
 * @file main.cpp
 * @author PehotinDO
 */

#include <cstdint>
#include "example_class.h"


int main()
{
	bool isErr = true;
	ExampleClass exampleObj;

	uint32_t factorialResult = exampleObj.computeFactorial(4);
	factorialResult = exampleObj.computeFactorial(6);

	static int32_t dstY[] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
	static int32_t a = -2;
	static int32_t srcX[] = {1, 1, 1, 1, 1, 1};
	static int32_t srcY[] = {4, 8, 15, 16, 23, 42};
	exampleObj.indexMax = exampleObj.computeAxpy(6, dstY, a, srcX, srcY);

	uint32_t checkIndexMax = exampleObj.findIndexMaxElement(10, dstY);
	isErr = exampleObj.indexMax != checkIndexMax ? true : false;

	return isErr;
}
