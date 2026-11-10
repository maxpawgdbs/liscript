(def max-x 1 max-y 1)
(def all-dirs ' ((1 2) (2 1) (-1 2) (2 -1) (1 -2) (-2 1) (-1 -2) (-2 -1)))

(defn iter (l d k)
    (cond (nil? d) nil
    (do (def x (car (car l)) y (car (cdr (car l))))
    (def x1 (car (car d)) y1 (car (cdr (car d))))
    (def res
        (cond (and (< 0 (+ x x1)) (<= (+ x x1) max-x) (< 0 (+ y y1)) (<= (+ y y1) max-y))
            (dfs (cons (list (+ x x1) (+ y y1)) l) (+ k 1))
            nil
        )
    )
    (cond (not (nil? res)) res (iter l (cdr d) k))
)))

(defn check (l k)
    (cond
        (contains? (car l) (cdr l))
            0
        (not (= k (* max-x max-y)))
            1
        l
    )
)

(defn dfs (l k)
    (def res (check l k))
    (cond
        (= res 0)
            nil
        (= res 1)
            (iter l all-dirs k)
        res
    )
)

((lambda (l) (cond (nil? l) l (append (reverse l) (cdr l))))(dfs ' ((1 1)) 1))