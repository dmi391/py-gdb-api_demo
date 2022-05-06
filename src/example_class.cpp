/**
 * @file example_class.cpp
 * @author PehotinDO
 */

#include "example_class.h"

uint32_t ExampleClass::mask = 0xFF;	///< Static field of ExampleClass


/**
 * @brief Constructor
 */
ExampleClass::ExampleClass()
{
	indexMax = 0xcf;
};


/**
 * @brief Маскирование числа маской ExampleClass::mask
 *
 * @param[in] val Исходное число
 * @return Маскированное значение
 *
 */
uint32_t ExampleClass::applyMask(uint32_t val)
{
	return (val & ExampleClass::mask);
}


/**
 * @brief Вычисление факториала числа
 *
 * @param[in] n Исходное число
 * @return Значение факториала
 *
 */
uint32_t ExampleClass::computeFactorial(uint32_t n)
{
	uint32_t factorial = 1;

	for(int i=1; i<=n; i=i+1)
	{
		factorial = factorial *  i;
	}
	return factorial;
}


/**
 * @brief Вычисление axpy
 * y = a*x + y, где x и y - векторы (массивы), a - число
 *
 * @param[in] len Длина векторов
 * @param[in] dstY Вектор-результат
 * @param[in] a Скаляр
 * @param[in] srcX Вектор x
 * @param[in] srcY Вектор y
 *
 */
uint32_t ExampleClass::computeAxpy(uint32_t len, int32_t* dstY, int32_t a, int32_t* srcX, int32_t* srcY)
{
	for(int i = 0; i < len; i++)
	{
		dstY[i] = a*srcX[i] + srcY[i];
	}

	return this->findIndexMaxElement(len, dstY); //Nested call
}


/**
 * @brief Нахождение индекса max элемента в массиве целых чисел
 *
 * @param[in] len Длина массива
 * @param[in] src Массив целых чисел
 * @return Индекс max элемента
 *
 */
uint32_t ExampleClass::findIndexMaxElement(uint32_t len, int32_t* src)
{
	uint32_t indexMax = 0;
	uint32_t max = src[0];

	for(uint32_t i = 0; i < len; i++)
	{
		if(src[i] >= max)
		{
			max = src[i];
			indexMax = i;
		}
	}
	return indexMax;
}


/**
 * @brief Метод, приводящий к exception
 *
 * @param[in] val Исходное число
 * @return Число*10
 *
 */
uint32_t ExampleClass::mustException(int32_t val)
{
	asm volatile ("ecall" :::);
	return (val * 10);
}
