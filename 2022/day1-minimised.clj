(def sorted-totals (sort (map #(reduce + %) (map #(map read-string %) (map clojure.string/split-lines (clojure.string/split (slurp "day1-input") #"\n\n"))))))
(println (last sorted-totals))  ; Part 1
(println (reduce + (take-last 3 sorted-totals)))  ; Part 2