I think this is the code that is used in the original system.  If it is, will you redraw the sequence diagram in light of this code?
```java
    private float degreeToAngle(float degree) {
        // TODO: move to constant

        int[] currentScale = {5, 10, 20, 40, 100};
        int range0 = currentScale[0];
        int range1 = currentScale[1] - currentScale[0];
        int range2 = currentScale[2] - currentScale[1];
        int range3 = currentScale[3] - currentScale[2];
        int range4 = currentScale[4] - currentScale[3];
        if (degree >= 0 && degree <= currentScale[0]) {
            return (offsetDegree / range0) * degree; -
        } else if (degree > currentScale[0] && degree <= currentScale[1]) {
            return offsetDegree + (stepDegree / range1) * (degree - currentScale[0]);
        } else if (degree > currentScale[1] && degree <= currentScale[2]) {
            return offsetDegree + stepDegree + (stepDegree / range2) * (degree - currentScale[1]);
        } else if (degree > currentScale[2] && degree <= currentScale[3]) {
            return offsetDegree + stepDegree * 2 + (stepDegree / range3) * (degree - currentScale[2]);
        } else if (degree > currentScale[3] && degree <= currentScale[4]) {
            return offsetDegree + stepDegree * 3 + (stepDegree / range4) * (degree - currentScale[3]);


        } else if (degree > -currentScale[0] && degree < 0) {
            return (offsetDegree / range0 * degree);
        } else if (degree > -currentScale[1] && degree <= -currentScale[0]) {
            return -offsetDegree + (stepDegree / range1) * (degree + currentScale[0]);
        } else if (degree > -currentScale[2] && degree <= -currentScale[1]) {
            return -offsetDegree - stepDegree + (stepDegree / range2) * (degree + currentScale[1]);
        } else if (degree > -currentScale[3] && degree <= -currentScale[2]) {
            return -offsetDegree - 2 * stepDegree + (stepDegree / range3) * (degree + currentScale[2]);
        } else if (degree >= -currentScale[4] && degree <= -currentScale[3]) {
            return -offsetDegree - 3 * stepDegree + (stepDegree / range4) * (degree + currentScale[3]);
        } else if (degree > currentScale[4]) {
            return (offsetDegree + 4 * stepDegree);
        } else if (degree < -currentScale[4])
            return -(offsetDegree + 4 * stepDegree);
        return 0;
    }
```