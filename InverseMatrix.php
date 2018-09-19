<?php
/**
 * Created by PhpStorm.
 * User: alexander
 * Date: 9/20/18
 * Time: 1:42 AM
 */

namespace App;

class InverseMatrix
{
    /**
     * @var array
     */
    private $matrix;

    /**
     * @var int|float
     */
    private $det;

    /**
     * InverseMatrix constructor.
     * @param array $matrix
     */
    public function __construct(array $matrix)
    {
        $matrixDem = new MatrixDet($matrix);
        $this->det = $matrixDem->getDet();
        $this->matrix = $matrix;
    }

    public function getInvertedMatrix(): array
    {
        $invMatrix = [];
        $counter = \count($this->matrix);

        for ($i = 0; $i < $counter; $i++) {
            for ($j = 0; $j < $counter; $j++) {

                $minor = [];
                $minorI = 0;

                for ($i1 = 0; $i1 < $counter; $i1++) {
                    $minorJ= 0;
                    if ($i1 === $i) {
                        continue;
                    }
                    for ($j1 = 0; $j1 < $counter; $j1++) {
                        if ($j1 === $j) {
                            continue;
                        }
                        $minor[$minorI][$minorJ] = $this->matrix[$i1][$j1];
                        $minorJ++;
                    }
                    $minorI++;
                }

                $minorDet = new MatrixDet($minor);
                $invMatrix[$j][$i] = ( (float) (-1) ** ($i + $j + 2) * $minorDet->getDet() ) / $this->det;
            }
        }

        return $invMatrix;
    }

    /**
     * @return array
     */
    public function getMatrix(): array
    {
        return $this->matrix;
    }
}
