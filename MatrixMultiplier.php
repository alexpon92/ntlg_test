<?php
/**
 * Created by PhpStorm.
 * User: alexander
 * Date: 9/20/18
 * Time: 1:00 AM
 */

namespace App;

class MatrixMultiplier
{
    /**
     * @var array
     */
    private $matrixA;

    /**
     * @var array
     */
    private $matrixB;

    /**
     * MatrixMultiplier constructor.
     * @param array $matrixA
     * @param array $matrixB
     * @throws \Exception
     */
    public function __construct(array $matrixA, array $matrixB)
    {
        $this->checkMatrixDimensions($matrixA, $matrixB);
        $this->matrixA = $matrixA;
        $this->matrixB = $matrixB;
    }

    /**
     * @param array $matrixA
     * @param array $matrixB
     * @throws \Exception
     */
    public function checkMatrixDimensions(array $matrixA, array $matrixB): void
    {
        $countIA = \count($matrixA);
        if ($countIA < 2) {
            throw new \Exception('Bad matrixA should be at least 2x2');
        }
        $countJA = \count($matrixA[0]);

        for ($i = 1; $i < $countIA; $i++) {
            if (\count($matrixA[$i]) !== $countJA) {
                throw new \Exception('Bad matrixA rows should have equal size');
            }
        }

        $countIB = \count($matrixB);
        if ($countIB < 2) {
            throw new \Exception('Bad matrixB should be at least 2x2');
        }
        $countJB = \count($matrixB[0]);

        for ($i = 1; $i < $countIB; $i++) {
            if (\count($matrixB[$i]) !== $countJB) {
                throw new \Exception('Bad matrixA rows should have equal size');
            }
        }

        if ($countJA !== $countIB) {
            throw new \Exception('MatrixA and MatrixB cannot be multiplied, dimensions mismatch');
        }
    }

    /**
     * @return array
     */
    public function multiply(): array
    {
        $result = [];
        $matrixARowCounter = \count($this->matrixA);
        $matrixBColumnCounter = \count($this->matrixB[0]);

        for ($i = 0; $i < $matrixARowCounter; $i++) {
            $result[$i] = [];
            $vectorA = $this->matrixA[$i];

            for ($j = 0; $j < $matrixBColumnCounter; $j++) {
                $vectorB = $this->getColumn($this->matrixB, $j);
                $result[$i][$j] = $this->scalarMultiply($vectorA, $vectorB);
            }
        }

        return $result;
    }


    /**
     * @param array $vectorA
     * @param array $vectorB
     * @return float|int
     */
    private function scalarMultiply(array $vectorA, array $vectorB)
    {
        $counter = \count($vectorA);
        $sum = 0;
        for ($i = 0; $i < $counter; $i++) {
            $sum += $vectorA[$i] * $vectorB[$i];
        }

        return $sum;
    }

    /**
     * @param array $matrix
     * @param int $columnNumber
     * @return array
     */
    private function getColumn(array $matrix, int $columnNumber): array
    {
        $counterI = \count($matrix);
        $counterJ = \count($matrix[0]);
        $vector = [];

        for ($i = 0; $i < $counterI; $i++) {
            for ($j = 0; $j < $counterJ; $j++) {
                if ($j === $columnNumber) {
                    $vector[] = $matrix[$i][$j];
                }
            }
        }

        return $vector;
    }

    /**
     * @return array
     */
    public function getMatrixA(): array
    {
        return $this->matrixA;
    }

    /**
     * @return array
     */
    public function getMatrixB(): array
    {
        return $this->matrixB;
    }


}
