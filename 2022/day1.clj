(require '[clojure.string :as str])
(def filename "input/1")
(def elves-rations (map #(map read-string %) (map str/split-lines (str/split (slurp filename) #"\n\n"))))
(def elves-totals (map #(reduce + %) elves-rations))
(def sorted-totals (sort elves-totals))
(println (last sorted-totals))  ; Part 1
(println (reduce + (take-last 3 sorted-totals)))  ; Part 2