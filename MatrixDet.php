<?php
/**
 * Created by PhpStorm.
 * User: alexander
 * Date: 9/20/18
 * Time: 12:00 AM
 */

namespace App;

class MatrixDet
{
    /**
     * @var array
     */
    private $matrix;

    /**
     * @var int|float
     */
    private $determinant;

    /**
     * MatrixDet constructor.
     * @param array $matrix
     * @throws \Exception
     */
    public function __construct(array $matrix)
    {
        if (!$this->checkMatrix($matrix)) {
            throw new \Exception('Matrix should be square');
        }

        $this->matrix = $matrix;
    }

    /**
     * @return int|float
     */
    public function getDet()
    {
        if (null === $this->determinant) {
            $this->determinant = $this->det($this->matrix);
        }

        return $this->determinant;
    }

    /**
     * @param array $matrix
     * @return int|float
     */
    private function det(array $matrix)
    {
        if (\count($matrix) === 2) {
            return $matrix[0][0] * $matrix[1][1] - $matrix[0][1] * $matrix[1][0];
        }

        $total = 0;

        $count = \count($matrix);

        for ($j = 0; $j < $count; $j++) {
            $minor = [];
            $minorI = 0;

            for ($i1 = 0; $i1 < $count; $i1++) {
                $minorJ= 0;
                if ($i1 === 0) {
                    continue;
                }
                for ($j1 = 0; $j1 < $count; $j1++) {
                    if ($j1 === $j) {
                        continue;
                    }
                    $minor[$minorI][$minorJ] = $matrix[$i1][$j1];
                    $minorJ++;
                }
                $minorI++;
            }
            $det = $this->det($minor, false);
            $total += (-1) ** ($j + 2) * $matrix[0][$j] * $det;
        }


        return $total;
    }

    /**
     * @param array $matrix
     * @return bool
     */
    private function checkMatrix(array $matrix): bool
    {
        $count = \count($matrix);

        for ($i = 0; $i < $count; $i++) {
            if (\count($matrix[$i]) !== $count) {
                return false;
            }
        }

        return true;
    }

    /**
     * @return array
     */
    public function getMatrix(): array
    {
        return $this->matrix;
    }
}
