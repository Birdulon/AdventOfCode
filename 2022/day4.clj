(require '[clojure.string :as str])
(def lines (str/split-lines (slurp "input/4")))
(def number-regex #"(?:(?<!\d)-)?\d+")
(defn parse-int [str] (Integer/valueOf str 10))
(defn get-numbers [line] (map parse-int (re-seq number-regex line)))
(def numbers (map get-numbers lines))
(defn range-within [s0 s1 t0 t1]  ;; either range is a subset of the other
    (or (<= t0 s0 s1 t1)
        (<= s0 t0 t1 s1)))
(defn range-overlaps [s0 s1 t0 t1]  ;; any range overlap
    (or (<= t0 s0 t1)
        (<= t0 s1 t1)
        (<= s0 t0 s1)
        (<= s0 t1 s1)))

;; Part 1 - one set is a subset of the other
(println (format "Part 1: %d elves have no unique work in their pairing"
    (count (filter identity (map #(apply range-within %) numbers)))))
;; Part 2 - any set overlap
(println (format "Part 2: %d elf pairs have overlapping work in their pairing"
    (count (filter identity (map #(apply range-overlaps %) numbers)))))
